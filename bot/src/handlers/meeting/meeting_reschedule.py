import re
from datetime import datetime, timedelta

from app import schedule_service_v1, user_service_v1
from core.constants import BotState, MeetingFormat
from decorators import at, t
from handlers.meeting.root_handlers import back_to_start_menu
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_START_MENU
from utils import context_manager as cm
from utils import make_message_handler, make_text_handler

from . import buttons
from .enums import States
from .helpers import context_manager
from .messages import (
    psychologist_meeting_message,
    user_check_meeting_message,
    user_choose_timeslot_message,
)


@t
def ask_for_reschedule(state: str):
    @at
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        keyboard = None
        chat_data_id = update.message.chat.id
        user = user_service_v1.get_user(chat_id=chat_data_id)
        meetings = schedule_service_v1.get_meetings_by_user(user_id=user.id, is_active="True")
        timeslots = schedule_service_v1.get_actual_timeslots()

        if not meetings:
            text_parts = ["У вас нет записи"]
            button = [[BTN_START_MENU]]
            keyboard = ReplyKeyboardMarkup(button, resize_keyboard=True)
            await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        if (
            datetime.strptime(meetings[0].date_start, "%d.%m.%Y %H:%M") - timedelta(hours=12)
            < datetime.now()
        ):
            text_parts = ["Ваша консультация:\n"]
            for index, meeting in enumerate(meetings):
                psychologist_profile = user_service_v1.get_user(id=meeting.psychologist)
                text_parts.append(
                    f"{psychologist_profile.first_name} {psychologist_profile.last_name} "
                )
                text_parts.append(f"{meeting.date_start}")
            text_parts += ["\nДо консультации осталось менее 12 часов, её невозможно перенести."]
            button = [[BTN_START_MENU]]
            keyboard = ReplyKeyboardMarkup(button, resize_keyboard=True)
            await update.message.reply_text(text="\n".join(text_parts), reply_markup=keyboard)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        if len(timeslots) < 2:
            text_parts = "Извините, сейчас нет подходящего времени для переноса записи."
            button = [[BTN_START_MENU]]
            keyboard = ReplyKeyboardMarkup(button, resize_keyboard=True)
            await update.message.reply_text(text="".join(text_parts), reply_markup=keyboard)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        if state == States.TYPING_MEETING_FORMAT:
            text_parts = "Выберите формат участия:"
            btns = [[buttons.BTN_MEETING_FORMAT_ONLINE, buttons.BTN_MEETING_FORMAT_OFFLINE]]
            keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)

        if state == States.TYPING_TIME_SLOT:
            meeting_format = update.message.text
            context_manager.set_meeting_format(context, meeting_format)
            meetings = schedule_service_v1.get_meetings_by_user(user=user.id, past="True")
            is_sixth_meeting = False
            if len(meetings) > 4:
                is_sixth_meeting = True
            psycho_set = {meeting.psychologist for meeting in meetings}
            timeslots = schedule_service_v1.get_actual_timeslots(is_free="True")
            timeslots = sorted(timeslots, key=lambda x: (x.profile.id not in psycho_set))
            text_parts = await user_choose_timeslot_message(
                timeslots, psycho_set, is_sixth_meeting=is_sixth_meeting
            )
            context_manager.set_timeslots(context, timeslots)

        if state == States.TYPING_MEETING_CONFIRM:
            number_of_timeslot = re.findall("\\d+", update.message.text) or []
            timeslots = context_manager.get_timeslots(context) or []
            if not number_of_timeslot or int(number_of_timeslot[0]) > len(timeslots):
                text = "Введен неправильный номер !\nНет таймслота под таким номером."
                await update.message.reply_text(text=text, reply_markup=keyboard)
                await back_to_start_menu(update, context)
                return BotState.STOPPING
            else:
                number_of_timeslot = int(number_of_timeslot[0])
            context_manager.set_timeslot_number(context, number_of_timeslot)
            meeting_format = context_manager.get_meeting_format(context)
            timeslots = context_manager.get_timeslots(context) or []
            timeslot = timeslots[number_of_timeslot - 1] if timeslots else {}
            context_manager.set_timeslot(context, timeslot)

            text_parts = await user_check_meeting_message(
                meeting_format,
                timeslot.profile.first_name,
                timeslot.profile.last_name,
                timeslot.date_start,
            )

            btns = [[buttons.BTN_CONFIRM_MEETING, buttons.BTN_NOT_CONFIRM_MEETING]]
            keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)

        context_manager.set_user(context, user)
        cm.set_meetings(context, meetings)

        if text_parts:
            await update.message.reply_text(text_parts, reply_markup=keyboard)
        else:
            text = "Извините, попробуйте ещё раз"
            await update.message.reply_text(text=text)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        return state

    return inner


@t
def meeting_update(confirm: bool):
    """Обновление записи пользователя"""

    @at
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if confirm:
            user = context_manager.get_user(context)
            timeslot = context_manager.get_timeslot(context)
            meeting_format = context_manager.get_meeting_format(context)
            meetings = cm.get_meetings(context)
            meeting = meetings[0]
            schedule_service_v1.update_meeting(
                date_start=str(datetime.strptime(timeslot.date_start, "%d.%m.%Y %H:%M")),
                psychologist_id=timeslot.profile.id,
                user_id=user.id,
                meeting_id=meeting.id,
                timeslot=timeslot.id,
                meeting_format=MeetingFormat.ONLINE
                if meeting_format == buttons.BTN_MEETING_FORMAT_ONLINE.text
                else MeetingFormat.OFFLINE,
            )

            psychologist_chat_id = timeslot.profile.chat_id
            if psychologist_chat_id:
                meeting_text = await psychologist_meeting_message(meeting_format, user, timeslot)
                await context.bot.send_message(chat_id=psychologist_chat_id, text=meeting_text)

            text = "Вы успешно записаны к психологу!"
        else:
            text = "Запись не оформлена!"

        await update.message.reply_text(text=text)

        await back_to_start_menu(update, context)

        return BotState.STOPPING

    return inner


meeting_reschedule_section = ConversationHandler(
    entry_points=[
        make_message_handler(
            buttons.BTN_MEETING_RESCHEDULE, ask_for_reschedule(States.TYPING_MEETING_FORMAT)
        ),
    ],
    states={
        States.TYPING_MEETING_FORMAT: [
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_ONLINE, ask_for_reschedule(States.TYPING_TIME_SLOT)
            ),
            make_message_handler(
                buttons.BTN_MEETING_FORMAT_OFFLINE, ask_for_reschedule(States.TYPING_TIME_SLOT)
            ),
        ],
        States.TYPING_TIME_SLOT: [
            make_text_handler(ask_for_reschedule(States.TYPING_MEETING_CONFIRM)),
        ],
        States.TYPING_MEETING_CONFIRM: [
            make_message_handler(buttons.BTN_CONFIRM_MEETING, meeting_update(True)),
            make_message_handler(buttons.BTN_NOT_CONFIRM_MEETING, meeting_update(False)),
        ],
    },
    fallbacks=[
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.MENU_MEETING_SELECTING_LEVEL,
    },
)
