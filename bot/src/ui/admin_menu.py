from request.clients import user_service
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from ui.buttons import (
    homme_button,
    list_admins_button,
    list_psychologists_button,
    test_button,
)
from ui.core import MenuNames


def admin_menu(update: Update, context: CallbackContext) -> None:
    if user_service.is_staff(telegramm_id=update.message.chat.id):
        buttons = ReplyKeyboardMarkup(
            [[homme_button], [list_admins_button], [list_psychologists_button], [test_button]],
            resize_keyboard=True,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=MenuNames.admin_menu.result.format(update.message.chat.first_name),
            reply_markup=buttons,
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Недостаточно прав для выполнения команды"
        )
