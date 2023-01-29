from handlers.admin.user_entrypoint import MENU_USERS_SELECTING_LEVEL
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_ADD_USER, BTN_ADMIN_MENU, BTN_DELETE_USER, BTN_SCHEDULE
from user_entrypoint import USER_GET_CLIENT


def get_user_list(script: int):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        user_list = USER_GET_CLIENT.get()
        users = [
            (f"{ind + 1} {user.telegram_id} {user.last_name} {user.first_name} {user.middle_name}")
            for ind, user in enumerate(user_list)
        ]
        buttons = [
            [BTN_ADD_USER, BTN_DELETE_USER, BTN_SCHEDULE],
            [
                BTN_ADMIN_MENU,
            ],
        ]
        keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
        await update.message.reply_text(text="\n".join(users), reply_markup=keyboard)

        return MENU_USERS_SELECTING_LEVEL

    return inner
