from request.clients import user_service
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from ui import MenuNames, admin_button, meeting_button, test_button


def main_menu(update: Update, context: CallbackContext) -> None:
    buttons = [[test_button], [meeting_button]]
    if user_service.is_staff(telegramm_id=update.message.chat.id):
        buttons.append([admin_button])
    keyboard = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuNames.start_menu.result.format(update.message.chat.first_name),
        reply_markup=keyboard,
    )
