from core.constants import BotState
from handlers.admin.questions import menu_answers, menu_questions
from handlers.admin.root_handlers import back_to_admin
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import (
    BTN_ADD_ANSWER,
    BTN_ADMIN_MENU,
    BTN_CHANGE_ANSWER,
    BTN_DELETE_ANSWER,
    BTN_QUESTIONS_MENU,
    BTN_SHOW_TESTS,
)
from utils import make_message_handler, make_text_handler

MENU_ANSWERS_SELECTING_LEVEL = "MENU_ANSWERS_SELECTING_LEVEL"
TYPING_ANSWER_ID_FOR_CHANGE_ANSWER = "TYPING_ANSWER_ID_FOR_CHANGE_ANSWER"
TYPING_ANSWER_TEXT_FOR_CHANGE_ANSWER = "TYPING_ANSWER_TEXT_FOR_CHANGE_ANSWER"
TYPING_ANSWER_TEXT_FOR_NEW_ANSWER = "TYPING_ANSWER_TEXT_FOR_NEW_ANSWER"
TYPING_ANSWER_VALUE_FOR_CHANGE_ANSWER = "TYPING_ANSWER_VALUE_FOR_CHANGE_ANSWER"
TYPING_ANSWER_VALUE_FOR_NEW_ANSWER = "TYPING_ANSWER_VALUE_FOR_CHANGE_ANSWER"
TYPING_ANSWER_ID_FOR_DELETE_ANSWER = "TYPING_ANSWER_ID_FOR_DELETE_ANSWER"
TYPING_CONFIRM_FOR_DELETE_TEST = "TYPING_CONFIRM_FOR_DELETE_TEST"

CREATING_NEW_ANSWER = "CREATING_NEW_ANSWER"

SCRIPT_CREATING_NEW_ANSWER, SCRIPT_CHANGE_ANSWER, SCRIPT_DELETE_ANSWER = range(3)


async def ask_for_answer_id(script: int = SCRIPT_CHANGE_ANSWER):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = "Введите ID варианта ответа:"
        await update.message.reply_text(text=text)
        if script == SCRIPT_DELETE_ANSWER:
            return TYPING_ANSWER_ID_FOR_DELETE_ANSWER
        return TYPING_ANSWER_ID_FOR_CHANGE_ANSWER

    return inner


async def ask_for_answer_text(script: int = SCRIPT_CREATING_NEW_ANSWER):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if script == SCRIPT_CHANGE_ANSWER:
            answer_id = update.message.text
            context.user_data["answer_id"] = answer_id
        text = "Введите текст варианта ответа (или '-' для отмены):"
        await update.message.reply_text(text=text)
        if script == SCRIPT_CREATING_NEW_ANSWER:
            return TYPING_ANSWER_TEXT_FOR_NEW_ANSWER
        return TYPING_ANSWER_TEXT_FOR_CHANGE_ANSWER

    return inner


async def ask_for_answer_value(script: int = SCRIPT_CREATING_NEW_ANSWER):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if script == SCRIPT_CHANGE_ANSWER:
            answer_text = update.message.text
            context.user_data["answer_text"] = answer_text
        text = "Введите количество баллов за этот вариант ответа:"
        await update.message.reply_text(text=text)
        if script == SCRIPT_CREATING_NEW_ANSWER:
            return TYPING_ANSWER_VALUE_FOR_NEW_ANSWER
        return TYPING_ANSWER_VALUE_FOR_CHANGE_ANSWER

    return inner


async def create_new_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    try:
        answer_value = int(update.message.text)
    except ValueError:
        await update.message.reply_text(text="Введите число")
        return TYPING_ANSWER_VALUE_FOR_NEW_ANSWER
    answer_text = context.user_data["answer_text"]
    # test_question_id = context.user_data["question_id"]
    answer_id = 0
    # TODO: создать вариант ответа с answer_text, answer_value
    text = f"Создан вариант ответа: '{answer_text}' (кол-во баллов: {answer_value}) ({answer_id})"
    await update.message.reply_text(text=text)
    await menu_answers(update, context)
    return MENU_ANSWERS_SELECTING_LEVEL


async def change_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    try:
        answer_value = int(update.message.text)
    except ValueError:
        await update.message.reply_text(text="Введите число")
        return TYPING_ANSWER_VALUE_FOR_CHANGE_ANSWER
    answer_text = context.user_data["answer_text"]
    answer_id = context.user_data["answer_id"]
    # test_question_id = context.user_data["question_id"]
    # TODO: изменить текст вопроса с question_id на question_text
    text = f"Новый вариант ответа с id {answer_id}: '{answer_text}' (кол-во баллов: {answer_value})"
    await update.message.reply_text(text=text)
    return MENU_ANSWERS_SELECTING_LEVEL


async def delete_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    # answer_id = update.message.text
    # TODO: убедиться в существовании answer_id
    answer = "not_None"
    if answer is not None:
        # TODO: удалить вариант ответа c answer_id
        text = "Вариант ответа удален!"
    else:
        text = "Вариант ответа с таким ID не найден."
    await update.message.reply_text(text=text)
    await menu_answers(update, context)
    return MENU_ANSWERS_SELECTING_LEVEL


answers_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_QUESTIONS_MENU, menu_answers),
    ],
    states={
        MENU_ANSWERS_SELECTING_LEVEL: [
            make_message_handler(BTN_SHOW_TESTS, menu_answers),
            make_message_handler(BTN_ADD_ANSWER, ask_for_answer_text(SCRIPT_CREATING_NEW_ANSWER)),
            make_message_handler(BTN_CHANGE_ANSWER, ask_for_answer_id(SCRIPT_CHANGE_ANSWER)),
            make_message_handler(BTN_DELETE_ANSWER, ask_for_answer_id(SCRIPT_DELETE_ANSWER)),
        ],
        CREATING_NEW_ANSWER: [
            make_text_handler(create_new_answer),
        ],
        TYPING_ANSWER_ID_FOR_CHANGE_ANSWER: [
            make_text_handler(ask_for_answer_text(SCRIPT_CHANGE_ANSWER))
        ],
        TYPING_ANSWER_TEXT_FOR_CHANGE_ANSWER: [
            make_text_handler(ask_for_answer_value(SCRIPT_CHANGE_ANSWER))
        ],
        TYPING_ANSWER_TEXT_FOR_NEW_ANSWER: [
            make_text_handler(ask_for_answer_value(SCRIPT_CREATING_NEW_ANSWER))
        ],
        TYPING_ANSWER_VALUE_FOR_CHANGE_ANSWER: [make_text_handler(change_answer)],
        TYPING_ANSWER_VALUE_FOR_NEW_ANSWER: [make_text_handler(create_new_answer)],
        TYPING_ANSWER_ID_FOR_DELETE_ANSWER: [make_text_handler(delete_answer)],
    },
    fallbacks=[
        make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        make_message_handler(BTN_QUESTIONS_MENU, menu_questions),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.MENU_TEST_SELECTING_LEVEL,
    },
)
