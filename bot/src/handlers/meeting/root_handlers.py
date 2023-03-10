from app import schedule_service_v1, user_service_v1
from core.constants import (
    MEETING_CURRENT_PRICE,
    MEETING_DURATION,
    MEETING_REGULAR_PRICE,
    BotState,
)
from core.settings import NUMBER_OF_FREE_MEETINGS
from handlers.root_handlers import start
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_START_MENU

from . import buttons


async def meetings_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    username = update.message.chat.username
    user = user_service_v1.get_user(username=username)
    number_of_user_meetings = len(schedule_service_v1.get_meetings_by_user(user=user.id))
    text = f"Длительность консультации психолога ({MEETING_DURATION}):\n"
    if number_of_user_meetings >= NUMBER_OF_FREE_MEETINGS:
        text += f"Сейчас {MEETING_CURRENT_PRICE} р.\n" f"Обычная цена {MEETING_REGULAR_PRICE} р.\n"
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
