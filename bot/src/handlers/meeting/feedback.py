from app import schedule_service_v1, user_service_v1
from core.constants import BotState
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_FEEDBACK, BTN_START_MENU
from utils import make_message_handler, make_text_handler

from .enums import States
from .helpers import context_manager
from .root_handlers import back_to_start_menu


def ask_for_feedback(state: str):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = ""
        keyboard = ""
        chat_data = update.message.chat
        telegram_login = chat_data.username
        user = user_service_v1.get_user(username=telegram_login)
        meetings = schedule_service_v1.get_meetings_by_user(user=user.id)
        if user is None:
            text = "Ваших данных нет в базе"
            await update.message.reply_text(text=text)
            await back_to_start_menu(update, context)
            return BotState.STOPPING
        if not meetings:
            text = "У вас еще небыло консультаций."
            await update.message.reply_text(text=text)
            await back_to_start_menu(update, context)
            return BotState.STOPPING

        if state == States.TYPING_MEETING_NUMBER:
            text = (
                "Введите порядковый номер консультации, "
                "для которой хотите оставить обратную связь"
            )
            for index, meeting in enumerate(meetings):
                psichologist = user_service_v1.get_user(id=meeting.psychologist)
                meeting_format = "Online" if meeting.format == 10 else "Очно"
                add_meeting = (
                    f"\n{index + 1}. {psichologist.first_name} "
                    f"{psichologist.last_name} "
                    f"{meeting.date_start} {meeting_format}. "
                    f"Тема: {meeting.comment[:30]}"
                )
                text += add_meeting
        elif state == States.CHECK_IS_FEEDBACK_LEFT:
            number_of_meeting = int(update.message.text)
            meeting = meetings[number_of_meeting - 1] if meetings else {}
            context_manager.set_meeting(context, meeting)
            feedback = schedule_service_v1.get_feedback_by_user_and_meeting(
                user=user.id,
                meeting=meeting.id,
            )
            if feedback:
                context_manager.set_feedback(context, feedback)
                feedback_text = feedback[0].text
                text = (
                    "Вы уже оставляли обратную связь для этой встречи: \n"
                    f"{feedback_text} \n"
                    "Введите текст обратной связи (мы обновим его)."
                )
            else:
                text = "Введите текст обратной связи:"
        elif state == States.TYPING_SCORE:
            feedback_text = update.message.text
            context_manager.set_feedback_text(context, feedback_text)
            text = "Оцените встречу от 1 до 10: \n" "Введите число"
        elif state == States.FEEDBACK_SAVED:
            score = update.message.text
            context_manager.set_score(context, score)
            feedback = context_manager.get_feedback(context)
            meeting = context_manager.get_meeting(context)
            feedback_text = context_manager.get_feedback_text(context)
            text = "Спасибо за ваш отзыв."
            if feedback:
                schedule_service_v1.update_feedback(
                    feedback_id=feedback[0].id, text=feedback_text, score=score
                )
            else:
                schedule_service_v1.create_feedback(
                    meeting_id=meeting.id, user_id=user.id, text=feedback_text, score=score
                )
            if user.id == meeting.user:
                psychologist_chat_id = user_service_v1.get_user(id=meeting.psychologist).chat_id
                meeting_format = "Онлайн" if meeting.format == 10 else "Очно"
                if psychologist_chat_id:
                    message = (
                        f"Вам оставлена обратная связь:\n\n"
                        f"Посетитель: {user.first_name} {user.last_name}\n"
                        f"Телефон: {user.phone}\n"
                        f"Когда: {meeting.date_start}\n"
                        f"Формат: {meeting_format}\n"
                    )
                    await context.bot.send_message(chat_id=psychologist_chat_id, text=message)
            await update.message.reply_text(text=text, reply_markup=keyboard)
            return BotState.END
        await update.message.reply_text(text=text, reply_markup=keyboard)

        return state

    return inner


feedback_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_FEEDBACK, ask_for_feedback(States.TYPING_MEETING_NUMBER)),
    ],
    states={
        States.TYPING_MEETING_NUMBER: [
            make_text_handler(ask_for_feedback(States.CHECK_IS_FEEDBACK_LEFT)),
        ],
        States.CHECK_IS_FEEDBACK_LEFT: [
            make_text_handler(ask_for_feedback(States.TYPING_SCORE)),
        ],
        States.TYPING_SCORE: [
            make_text_handler(ask_for_feedback(States.FEEDBACK_SAVED)),
        ],
    },
    fallbacks=[
        make_message_handler(BTN_START_MENU, back_to_start_menu),
    ],
    map_to_parent={
        BotState.END: BotState.MENU_START_SELECTING_LEVEL,
    },
)
