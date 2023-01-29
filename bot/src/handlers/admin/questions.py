from core.constants import BotState
from handlers.admin.answers import answers_section
from handlers.admin.root_handlers import back_to_admin
from handlers.admin.tests import menu_tests
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import (
    BTN_ADD_ANSWER,
    BTN_ADD_QUESTION,
    BTN_ADMIN_MENU,
    BTN_CHANGE_ANSWER,
    BTN_CHANGE_QUESTION,
    BTN_DELETE_ANSWER,
    BTN_DELETE_QUESTION,
    BTN_QUESTIONS_MENU,
    BTN_SHOW_TESTS,
    BTN_TESTS_MENU,
)
from utils import context_manager, make_message_handler, make_text_handler

MENU_ANSWERS_SELECTING_LEVEL = "MENU_ANSWERS_SELECTING_LEVEL"
MENU_QUESTIONS_SELECTING_LEVEL = "MENU_QUESTIONS_SELECTING_LEVEL"
MENU_TESTS_LIST_SELECTING_LEVEL = "MENU_TESTS_LIST_SELECTING_LEVEL"
TYPING_QUESTION_TEXT_FOR_CHANGE_QUESTION = "TYPING_QUESTION_TEXT_FOR_CHANGE_QUESTION"
TYPING_QUESTION_ID_FOR_CHANGE_QUESTION = "TYPING_QUESTION_ID_FOR_CHANGE_QUESTION"
TYPING_QUESTION_ID_FOR_DELETE_QUESTION = "TYPING_QUESTION_ID_FOR_DELETE_QUESTION"
TYPING_CONFIRM_FOR_DELETE_TEST = "TYPING_CONFIRM_FOR_DELETE_TEST"

CREATING_NEW_QUESTION = "CREATING_NEW_QUESTION"

SCRIPT_CREATING_NEW_QUESTION, SCRIPT_CHANGE_QUESTION, SCRIPT_DELETE_QUESTION = range(3)


async def menu_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    test_id = context_manager.get_test_id(context)
    test = test_id
    test.name = str(test_id)  # TODO: получить тест по test_id
    header = f"Редактирование вопросов теста {test.name}"
    questions = []  # TODO: получить список вопросов теста
    questions_info = "/n".join(
        [f"{n}. {q.order_num} {q.text} ({q.id})" for n, q in enumerate(questions)]
    )
    text = "/n".join([header, questions_info])
    buttons = [
        [BTN_ADD_QUESTION, BTN_CHANGE_QUESTION, BTN_DELETE_QUESTION],
        [BTN_TESTS_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    await update.message.reply_text(text, reply_markup=keyboard)
    return MENU_QUESTIONS_SELECTING_LEVEL


async def menu_answers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    question_id = context_manager.get_question_id(context)
    question = question_id
    question.text = str(question_id)  # TODO: получить вопрос по question_id
    header = f"Редактирование ответов на вопрос '{question.text}'"
    answers = []  # TODO: получить список ответов на вопрос
    answers_info = "/n".join(
        [f"{n}. {a.text} (Баллов: {a.value}) ({a.id})" for n, a in enumerate(answers)]
    )
    text = "/n".join([header, answers_info])
    buttons = [
        [BTN_ADD_ANSWER, BTN_CHANGE_ANSWER, BTN_DELETE_ANSWER],
        [BTN_QUESTIONS_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=keyboard)

    return MENU_ANSWERS_SELECTING_LEVEL


async def ask_for_question_id(script: int = SCRIPT_CHANGE_QUESTION):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = "Введите ID вопроса:"
        await update.message.reply_text(text=text)
        if script == SCRIPT_DELETE_QUESTION:
            return TYPING_QUESTION_ID_FOR_DELETE_QUESTION
        return TYPING_QUESTION_ID_FOR_CHANGE_QUESTION

    return inner


async def ask_for_question_text(script: int = SCRIPT_CREATING_NEW_QUESTION):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if script == SCRIPT_CHANGE_QUESTION:
            question_id = update.message.text
            context.user_data["question_id"] = question_id
        text = "Введите текст вопроса (или '-' для отмены):"
        await update.message.reply_text(text=text)
        if script == SCRIPT_CREATING_NEW_QUESTION:
            return CREATING_NEW_QUESTION
        return TYPING_QUESTION_TEXT_FOR_CHANGE_QUESTION

    return inner


async def create_new_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    question_text = update.message.text
    if question_text == "-":
        text = "Создание вопроса отменено"
    else:
        # TODO: создать вопрос с текстом question_text
        question_id = 0
        text = f"Успешно созданному вопросу '{question_text}' присвоен id: {question_id}"
    await update.message.reply_text(text=text)
    context.user_data["question_id"] = question_id
    menu_answers(update, context)
    return MENU_ANSWERS_SELECTING_LEVEL


async def change_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    question_text = update.message.text
    question_id = context.user_data["question_id"]
    if question_text == "-":
        text = "Редактирование вопроса отменено"
    else:
        # TODO: изменить текст вопроса с question_id на question_text
        question_id = 0
        text = f"Текст вопроса с id {question_id} успешно изменен на '{question_text}'"
    await update.message.reply_text(text=text)
    return MENU_ANSWERS_SELECTING_LEVEL


async def delete_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    # question_id = update.message.text
    # TODO: убедиться в существовании question_id
    question = "not_None"
    if question is not None:
        # TODO: удалить вопрос c question_id
        text = "Вопрос удален!"
    else:
        text = "Вопрос с таким ID не найден."

    await update.message.reply_text(text=text)
    await menu_questions(update, context)
    return MENU_QUESTIONS_SELECTING_LEVEL


questions_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_QUESTIONS_MENU, menu_questions),
    ],
    states={
        MENU_QUESTIONS_SELECTING_LEVEL: [
            make_message_handler(BTN_SHOW_TESTS, menu_tests),
            make_message_handler(
                BTN_ADD_QUESTION, ask_for_question_text(SCRIPT_CREATING_NEW_QUESTION)
            ),
            make_message_handler(BTN_CHANGE_QUESTION, ask_for_question_id(SCRIPT_CHANGE_QUESTION)),
            make_message_handler(BTN_DELETE_QUESTION, ask_for_question_id(SCRIPT_DELETE_QUESTION)),
        ],
        CREATING_NEW_QUESTION: [
            make_text_handler(create_new_question),
        ],
        TYPING_QUESTION_ID_FOR_CHANGE_QUESTION: [
            make_text_handler(ask_for_question_text(SCRIPT_CHANGE_QUESTION))
        ],
        TYPING_QUESTION_TEXT_FOR_CHANGE_QUESTION: [make_text_handler(change_question)],
        TYPING_QUESTION_ID_FOR_DELETE_QUESTION: [make_text_handler(delete_question)],
        MENU_ANSWERS_SELECTING_LEVEL: [answers_section],
    },
    fallbacks=[
        make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        make_message_handler(BTN_QUESTIONS_MENU, menu_questions),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.MENU_ADMIN_SELECTING_LEVEL,
    },
)
