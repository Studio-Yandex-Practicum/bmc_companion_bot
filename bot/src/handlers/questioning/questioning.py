from core.constants import BotState
from request.exceptions import NoNextQuestion
from schemas.requests import (
    UserTestQuestionAnswerSpecificRequest,
    UserTestSpecificRequest,
)
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters
from ui.buttons import BTN_START_MENU
from utils import ContextManager

from .root_handlers import api_client, questioning_section


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = ContextManager.get_user_id(context)
    test_id = ContextManager.get_test_id(context)
    test_result = api_client.test_result(UserTestSpecificRequest(user_id=user_id, test_id=test_id))
    await update.message.reply_text(
        f"В тесте «{test_result.name}» вы набрали {test_result.value} баллов."
    )
    ContextManager.set_test_id(context, None)
    bot_state = await questioning_section(update, context)
    return bot_state


async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = ContextManager.get_user_id(context)
    test_id = ContextManager.get_test_id(context)
    try:
        next_question = api_client.next_question(
            UserTestSpecificRequest(user_id=user_id, test_id=test_id)
        )
        ContextManager.set_question_id(context, next_question.test_question_id)
    except NoNextQuestion:
        ContextManager.set_question_id(context, None)
        bot_state = await show_result(update, context)
        return bot_state
    buttons = []
    ContextManager.set_answers(context, {})
    answers = next_question.answers.items
    for answer in answers:
        print(answer)
        buttons.append(KeyboardButton(text=answer.text))
        ContextManager.get_answers(context)[answer.text] = answer.answer_id
    buttons = [buttons, [BTN_START_MENU]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    ContextManager.set_keys(context, keyboard)
    await update.message.reply_text(next_question.text, reply_markup=keyboard)
    return BotState.QUESTIONING


async def submit_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer_text = update.message.text
    if answer_text not in ContextManager.get_answers(context):
        await update.message.reply_text(
            "Выберите ответ из предложенных вариантов",
            reply_markup=ContextManager.get_keys(context),
        )
        return BotState.QUESTIONING
    answer_id = ContextManager.get_answers(context)[answer_text]
    api_client.submit_answer(
        UserTestQuestionAnswerSpecificRequest(
            user_id=ContextManager.get_user_id(context),
            test_id=ContextManager.get_test_id(context),
            test_question_id=ContextManager.get_question_id(context),
            answer_id=answer_id,
        )
    )
    bot_state = await next_question(update, context)
    return bot_state


question_handler = MessageHandler(~filters.Regex(BTN_START_MENU.text), submit_answer)
