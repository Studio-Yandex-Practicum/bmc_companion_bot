from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from . import constants as const


class MenuElement:
    def __init__(self, name, result, answers):
        self.name = name
        self.result = result
        self.answers = answers

    def __call__(self, answer_name: str) -> str:
        return self.answers[answer_name]


class MenuNames:
    """Текстовое описание для элементов меню."""

    start_menu = MenuElement(
        name=const.NAME,
        result=const.GREETING_MESSAGE,
        answers=const.ANSWERS,
    )


def main_menu(update: Update, context: CallbackContext):
    buttons = ReplyKeyboardMarkup(
        [[MenuNames.start_menu("to_test")], [MenuNames.start_menu("to_meeting")]],
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuNames.start_menu.result.format(update.message.chat.first_name),
        reply_markup=buttons,
    )
