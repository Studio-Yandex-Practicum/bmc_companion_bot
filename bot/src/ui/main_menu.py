from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from ui import MenuNames


def main_menu(update: Update, context: CallbackContext) -> None:
    buttons = ReplyKeyboardMarkup(
        [[MenuNames.start_menu("to_test")], [MenuNames.start_menu("to_meeting")]],
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuNames.start_menu.result.format(update.message.chat.first_name),
        reply_markup=buttons,
    )
