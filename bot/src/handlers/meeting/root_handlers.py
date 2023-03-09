from app import schedule_service_v1, user_service_v1
from core.constants import MEETING_PRICE, BotState
from handlers.root_handlers import start
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_START_MENU

from . import buttons


async def meetings_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    username = update.message.chat.username
    user = user_service_v1.get_user(username=username)
    number_of_user_meetings = len(schedule_service_v1.get_meetings_by_user(user=user.id))
    text = "Длительность консультации психолога (50 мин.):\n"
    if number_of_user_meetings >= 5:
        text += f"Сейчас {MEETING_PRICE} р.\n" "Обычная цена 2000 р.\n"
    text += "Выберите, что нужно сделать:"
    btns = [
        [
            buttons.BTN_MEETING_FIRST,
            buttons.BTN_MEETING_REPEAT,
            buttons.BTN_MEETING_CANCEL,
            buttons.BTN_MEETING_RESCHEDULE,
        ],
        [BTN_START_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(btns, one_time_keyboard=True)
    await update.message.reply_text(text, reply_markup=keyboard)
    return BotState.MENU_MEETING_SELECTING_LEVEL


async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await start(update, context)
    return BotState.END
