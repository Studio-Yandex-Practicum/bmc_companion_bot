from core.constants import BotState
from decorators import at
from handlers.questioning.root_handlers import api_client, test_questioning_section
from request.exceptions import NoNextQuestion
from schemas.requests import (
    UceTestRequest,
    UserTestQuestionAnswerSpecificRequest,
    UserTestSpecificRequest,
)
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters
from ui.buttons import BTN_START_MENU
from utils import context_manager


@at
async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = context_manager.get_user_id(context)
    test_id = context_manager.get_test_id(context)
    if not test_id:
        return await test_questioning_section(update, context)
    test_result = api_client.test_result(UserTestSpecificRequest(user_id=user_id, test_id=test_id))
    uce_test_id = api_client.uce_test_id(UceTestRequest()).id
    text = f"В тесте «{test_result.name}» вы набрали {test_result.value} баллов."
    if test_id == uce_test_id:
        text += "\nРекомендуем записаться на консультацию!"
    context_manager.set_test_id(context, None)
    await update.message.reply_text(text)
    bot_state = await test_questioning_section(update, context)
    return bot_state


@at
async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_id = context_manager.get_user_id(context)
    test_id = context_manager.get_test_id(context)
    try:
        next_question = api_client.next_question(
            UserTestSpecificRequest(user_id=user_id, test_id=test_id)
        )
        context_manager.set_question_id(context, next_question.id)
    except NoNextQuestion:
        context_manager.set_question_id(context, None)
        bot_state = await show_result(update, context)
        return bot_state
    buttons = []
    context_manager.set_answers(context, {})
    answers = next_question.answers.items
    for answer in answers:
        buttons.append(KeyboardButton(text=answer.text))
        context_manager.get_answers(context)[answer.text] = answer.id
    buttons = [buttons, [BTN_START_MENU]]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    context_manager.set_keys(context, keyboard)
    await update.message.reply_text(next_question.text, reply_markup=keyboard)
    return BotState.QUESTIONING


@at
async def submit_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer_text = update.message.text
    answers = context_manager.get_answers(context)
    if not answers:
        bot_state = await show_result(update, context)
        return bot_state
    if answer_text not in context_manager.get_answers(context):
        await update.message.reply_text(
            "Выберите ответ из предложенных вариантов",
            reply_markup=context_manager.get_keys(context),
        )
        return BotState.QUESTIONING
    answer_id = context_manager.get_answers(context)[answer_text]
    api_client.submit_answer(
        UserTestQuestionAnswerSpecificRequest(
            user_id=context_manager.get_user_id(context),
            test_id=context_manager.get_test_id(context),
            question_id=context_manager.get_question_id(context),
            answer_id=answer_id,
        )
    )
    bot_state = await next_question(update, context)
    return bot_state


question_handler = MessageHandler(~filters.Regex(BTN_START_MENU.text), submit_answer)
