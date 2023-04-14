from datetime import datetime as dt

from app import schedule_service_v1, user_service_v1
from core.constants import BotState
from handlers.root_handlers import start
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_START_MENU

from . import buttons


async def meetings_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Выберите, что нужно сделать:"
    chat_data_id = update.message.chat.id
    user = user_service_v1.get_user(chat_id=chat_data_id)
    meetings = schedule_service_v1.get_meetings_by_user(user_id=user.id, is_active="True")
    meetings = [i for i in meetings if dt.strptime(i.date_start, "%d.%m.%Y %H:%M") > dt.now()]
    past_meetings = schedule_service_v1.get_meetings_by_user(user_id=user.id, past="True")
    if meetings:
        btns = [[buttons.BTN_MEETING_CANCEL, buttons.BTN_MEETING_RESCHEDULE], [BTN_START_MENU]]
    else:
        if past_meetings:
            btns = [[buttons.BTN_MEETING_REPEAT], [BTN_START_MENU]]
        else:
            btns = [
                [
                    buttons.BTN_MEETING_FIRST,
                ],
                [BTN_START_MENU],
            ]
    # btns += [BTN_START_MENU]
    keyboard = ReplyKeyboardMarkup(btns, resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=keyboard)
    return BotState.MENU_MEETING_SELECTING_LEVEL


async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await start(update, context)
    return BotState.END
