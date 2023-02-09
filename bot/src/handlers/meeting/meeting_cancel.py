from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from app import schedule_service_v1, user_service_v1

from . import buttons
from .enums import States
from .root_handlers import choose_meeting_move, back_to_start_menu
from .helpers import context_manager
from utils import make_message_handler, make_text_handler
from core.constants import BotState

from ui.buttons import BTN_START_MENU


def ask_for_delete(state: str):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = 'Выберите запись, которую нужно отменить:\n'
        meetings = schedule_service_v1.get_meetings()
        for index, meeting in enumerate(meetings):
            text += (
                f'\n{index + 1}. {meeting.user.first_name}'
                f'{meeting.user.last_name} '
                f'{meeting.date_start}'
            )
        context_manager.set_actual_meeting(context, meeting)
        button = [
            [buttons.BTN_MEETING_CANCEL],
            [buttons.BTN_MEETING_RESCHEDULE],
            [BTN_START_MENU]
        ]
        keyboard = ReplyKeyboardMarkup(button, one_time_keyboard=True)
        await update.message.reply_text(text=text, reply_markup=keyboard)
        return state

    return inner


def cancel_meeting():
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = 'Запись отменена'
        meeting = context_manager.get_actual_meeting(context)
        user_text = 'Ваша запись успешно отменена.'
        psyhologist_text = (
            f'Отмена записи:\n'
            f'{meeting.user.last_name} '
            f'{str(meeting.user.first_name)[0]}.'
            f'{str(meeting.user.middle_name)[0]}.\n'
            f'{meeting.user.phone}\n'
            f'{meeting.date_start}'
        )

        await schedule_service_v1.meeting_cancel(meeting)
        context.bot.send_message(
            chat_id=meeting.user.chat_id,
            text=user_text
        )
        context.bot.send_message(
            chat_id=meeting.psychologist.chat_id,
            text=psyhologist_text
        )
        await update.message.reply_text(text=text)

        await back_to_start_menu(update, context)

        return BotState.STOPPING

    return inner


def meeting_reschedule():
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = 'Выберите новую запись'
        meeting = context_manager.get_actual_meeting(context)
        psyhologist_text = (
            f'Отмена записи:\n'
            f'{meeting.user.last_name} '
            f'{str(meeting.user.first_name)[0]}.'
            f'{str(meeting.user.middle_name)[0]}.\n'
            f'{meeting.user.phone}\n'
            f'{meeting.date_start}'
        )

        await schedule_service_v1.meeting_cancel(meeting)
        context.bot.send_message(
            chat_id=meeting.psychologist.chat_id,
            text=psyhologist_text
        )
        await update.message.reply_text(text=text)

        # вызов функции повторной записи

        return BotState.STOPPING

    return inner


meeting_cancel_section = ConversationHandler(
    entry_points=[
        make_message_handler(buttons.BTN_MEETING_CANCEL, ask_for_delete(States.CHOOSE_MEETING))
    ],
    states={
        States.TYPING_MEETING_CANCEL: [
            make_message_handler(buttons.BTN_MEETING_DELETE, cancel_meeting),
            make_message_handler(buttons.BTN_MEETING_RESCHEDULE, meeting_reschedule)
        ]
    },
    fallbacks=[
        # make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        # make_message_handler(BTN_TESTS_MENU, menu_tests),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
    },
)




