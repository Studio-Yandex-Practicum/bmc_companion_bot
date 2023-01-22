from core.constants import BotState
from request.exceptions import NoNextQuestion
from schemas.requests import (
    UserTestQuestionAnswerSpecificRequest,
    UserTestSpecificRequest,
)
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters
from ui.buttons import BTN_START_MENU

from .root_handlers import api_client, questioning_section


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = context.user_data["current_user_id"]
    test_id = context.user_data["current_test_id"]
    test_result = api_client.test_result(UserTestSpecificRequest(user_id=user_id, test_id=test_id))
    await update.message.reply_text(
        f"В тесте «{test_result.name}» вы набрали {test_result.value} баллов."
    )
    context.user_data["current_test_id"] = None
    bot_state = await questioning_section(update, context)
    return bot_state


async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = context.user_data["current_user_id"]
    test_id = context.user_data["current_test_id"]
    try:
        next_question = api_client.next_question(
            UserTestSpecificRequest(user_id=user_id, test_id=test_id)
        )
        context.user_data["current_question_id"] = next_question.test_question_id
    except NoNextQuestion:
        context.user_data["current_question_id"] = None
        bot_state = await show_result(update, context)
        return bot_state
    buttons = []
    context.chat_data["answer_list"] = {}
    answers = next_question.answers.__root__
    for answer in answers:
        buttons.append(KeyboardButton(text=answer.text))
        context.chat_data["answer_list"][answer.text] = answer.answer_id
    buttons = [buttons, [BTN_START_MENU]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context.chat_data["current_keyboard"] = keyboard
    await update.message.reply_text(next_question.text, reply_markup=keyboard)
    return BotState.QUESTIONING


async def submit_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer_text = update.message.text
    if answer_text not in context.chat_data["answer_list"]:
        await update.message.reply_text(
            "Выберите ответ из предложенных вариантов",
            reply_markup=context.chat_data["current_keyboard"],
        )
        return BotState.QUESTIONING
    answer_id = context.chat_data["answer_list"][answer_text]
    api_client.submit_answer(
        UserTestQuestionAnswerSpecificRequest(
            user_id=context.user_data["current_user_id"],
            test_id=context.user_data["current_test_id"],
            test_question_id=context.user_data["current_question_id"],
            answer_id=answer_id,
        )
    )
    bot_state = await next_question(update, context)
    return bot_state


question_handler = MessageHandler(~filters.Regex(BTN_START_MENU.text), submit_answer)
