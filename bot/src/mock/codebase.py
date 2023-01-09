from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler, Filters, MessageHandler
from ui import MenuNames

ANSWER, CHOICE, TESTING = range(3)


def choose_test(update: Update, context: CallbackContext) -> None:
    tests = context.bot_data["tests"]
    buttons_layout = [[test["name"]] for test in tests]
    buttons = ReplyKeyboardMarkup(
        buttons_layout,
        resize_keyboard=True,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuNames.test_menus.result,
        reply_markup=buttons,
    )


def test_menu(update: Update, context: CallbackContext):
    choose_test(update, context)
    return CHOICE


def start_test(update, context):
    ask_question(update, context)
    return ANSWER


def ask_question(update, context):
    active_test = context.user_data["active_test"]
    active_question = context.user_data["active_question"]
    question = active_test["questions"][active_question]
    answers = [
        ". ".join([str(i + 1), answer["text"]]) for i, answer in enumerate(question["answers"])
    ]
    keyboard = [answers]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(question["text"], reply_markup=reply_markup)


def show_result(update, context):
    score = context.user_data["current_score"]
    keyboard = [["Пройти тестирование", "Записаться к психологу"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        f"Тест закончен! Вы набрали {score} баллов.", reply_markup=reply_markup
    )


def process_answer(update, context):
    user_answer = update.message.text.split(". ")[1]
    active_test = context.user_data["active_test"]
    active_question = context.user_data["active_question"]
    for answer in active_test["questions"][active_question]["answers"]:
        if user_answer == answer["text"]:
            context.user_data["current_score"] += answer["value"]
    context.user_data["active_question"] += 1
    if context.user_data["active_question"] == len(active_test["questions"]):
        show_result(update, context)
        return ConversationHandler.END
    ask_question(update, context)
    return ANSWER


def test_choice(update, context):
    answer = update.message.text
    tests = context.bot_data["tests"]
    for test in tests:
        if test["name"] == answer:
            context.user_data["active_test"] = test
            context.user_data["active_question"] = 0
            context.user_data["current_score"] = 0
            n_quest = len(test["questions"])
            break
    keyboard = [[KeyboardButton("Начать тестирование")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text(
        f"Вы решили пройти тест «{answer}».\n" f"Вам предстоит ответить на {n_quest} вопросов",
        reply_markup=reply_markup,
    )
    return TESTING


question_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("Начать тестирование"), start_test)],
    fallbacks=[],
    states={
        ANSWER: [MessageHandler(Filters.text, process_answer)],
    },
)

choose_test_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("Тесты"), test_menu)],
    fallbacks=[MessageHandler(Filters.regex("Пройти тестирование"), test_menu)],
    states={CHOICE: [MessageHandler(Filters.text, test_choice)], TESTING: [question_handler]},
)
