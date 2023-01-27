from core.constants import BotState
from handlers.meeting.root_handlers import back_to_start_menu
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import BTN_MEETING_FIRST
from utils import context_manager, make_message_handler, make_text_handler

BTN_I_DONT_KNOW = KeyboardButton(text="Не знаю")
BTN_MEETING_FORMAT_ONLINE = KeyboardButton(text="Online")
BTN_MEETING_FORMAT_OFFLINE = KeyboardButton(text="Очно")
BTN_CONFIRM_MEETING = KeyboardButton(text="Записаться")
BTN_NOT_CONFIRM_MEETING = KeyboardButton(text="Не записываться")

DO_NOTHING_SIGN = "-"

TYPING_PHONE = "TYPING_PHONE"
TYPING_FIRST_NAME = "TYPING_FIRST_NAME"
TYPING_LAST_NAME = "TYPING_LAST_NAME"
TYPING_AGE = "TYPING_AGE"
TYPING_TEST_SCORE = "TYPING_TEST_SCORE"
TYPING_MEETING_FORMAT = "TYPING_MEETING_FORMAT"
TYPING_TIME_SLOT = "TYPING_TIME_SLOT"
TYPING_MEETING_CONFIRM = "TYPING_MEETING_CONFIRM"

CONTEXT_KEY_FORMAT = "CONTEXT_KEY_FORMAT"
CONTEXT_KEY_TIMESLOT = "CONTEXT_KEY_TIMESLOT"
CONTEXT_EXISTING_TIMESLOT = "CONTEXT_EXISTING_TIMESLOT"


def ask_for_input(state: str):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = ""
        keyboard = None

        # TODO: пытаемся получить юзера из контекста или найти юзера по telegram логину
        user = context_manager.get_user(context)
        if user is None:
            # TODO: если юзера нет в контексте, то пытаемся найти юзера по telegram логину
            user = {
                "phone": "99",
                "first_name": "Denis",
                "last_name": "",
            }

        user = user or {}
        phone = user.get("phone")
        first_name = user.get("first_name")
        last_name = user.get("last_name")
        age = user.get("age")

        if state == TYPING_PHONE:
            text = "Введите номер телефона"
            text += (
                ":" if not phone else f" (или введите {DO_NOTHING_SIGN}, чтобы оставить {phone}):"
            )
        elif state == TYPING_FIRST_NAME:
            phone = update.message.text
            if phone != DO_NOTHING_SIGN:
                # TODO: обновить телефон юзера в БД
                pass

            text = "Как Вас зовут? Введите только имя"
            text += (
                ":"
                if not first_name
                else f" (или введите {DO_NOTHING_SIGN}, чтобы оставить {first_name}):"
            )
        elif state == TYPING_LAST_NAME:
            first_name = update.message.text
            if first_name != DO_NOTHING_SIGN:
                # TODO: обновить first_name юзера в БД
                pass

            text = "Введите фамилию"
            text += (
                ":"
                if not last_name
                else f" (или введите {DO_NOTHING_SIGN}, чтобы оставить {last_name}):"
            )
        elif state == TYPING_AGE:
            last_name = update.message.text
            if last_name != DO_NOTHING_SIGN:
                # TODO: обновить last_name юзера в БД
                pass

            text = "Введите возраст"
            text += ":" if not age else f" (или введите {DO_NOTHING_SIGN}, чтобы оставить {age}):"
        elif state == TYPING_TEST_SCORE:
            age = update.message.text
            if age != DO_NOTHING_SIGN:
                # TODO: обновить last_name юзера в БД
                pass

            # TODO: получить балл за тест НДО с помощью функции get_uce_score (см. задачу)
            test_score = 0
            if test_score == 0:
                text = "Какой у Вас балл за тест НДО:"
                buttons = [
                    [BTN_I_DONT_KNOW],
                ]
                keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
            else:
                text = "Выберите формат записи:"
        elif state == TYPING_MEETING_FORMAT:
            text = "Выберите формат участия:"
            buttons = [
                [BTN_MEETING_FORMAT_ONLINE, BTN_MEETING_FORMAT_OFFLINE],
            ]
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
        elif state == TYPING_TIME_SLOT:
            meeting_format = update.message.text
            context_manager.set(context, CONTEXT_KEY_FORMAT, meeting_format)

            text = "Выберите дату и время записи:\n"
            # TODO: получить таймслоты
            timeslots = [
                {
                    "fio": "Иванов Иван",
                    "date": "01.01.2023 01:00",
                },
                {
                    "fio": "Иванов Иван",
                    "date": "01.01.2023 18:00",
                },
                {
                    "fio": "Петров Андрей",
                    "date": "02.01.2023 14:00",
                },
            ]
            context_manager.set(context, CONTEXT_EXISTING_TIMESLOT, timeslots)

            for index, value in enumerate(timeslots):
                text += f"\n{index + 1}. {value.get('fio')} {value.get('date')}"
        elif state == TYPING_MEETING_CONFIRM:
            number_of_timeslot = int(update.message.text)
            # TODO: добавить запись в таблицу митингов

            meeting_format = context_manager.get(context, CONTEXT_KEY_FORMAT)
            timeslots = context_manager.get(context, CONTEXT_EXISTING_TIMESLOT) or []
            timeslot = timeslots[number_of_timeslot - 1] if timeslots else {}

            text = "Давайте все проверим:\n"
            text += f"\nФормат записи: {meeting_format}"
            text += f"\nПсихолог: {timeslot.get('fio')}"
            text += f"\nДата: {timeslot.get('date')}"

            buttons = [
                [BTN_CONFIRM_MEETING, BTN_NOT_CONFIRM_MEETING],
            ]
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

        context_manager.set_user(context, user)

        await update.message.reply_text(text=text, reply_markup=keyboard)

        return state

    return inner


async def go_to_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "выполняется переход на прохождение теста НДО:"
    await update.message.reply_text(text)
    return "---"


def process_meeting_confirm(confirm: bool):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if confirm:
            text = "Вы успешно записаны к психологу!"
        else:
            text = "Запись не оформлена!"

        await update.message.reply_text(text=text)

        await back_to_start_menu(update, context)

        return BotState.STOPPING

    return inner


meeting_first_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_MEETING_FIRST, ask_for_input(TYPING_PHONE)),
    ],
    states={
        TYPING_PHONE: [
            make_text_handler(ask_for_input(TYPING_FIRST_NAME)),
        ],
        TYPING_FIRST_NAME: [
            make_text_handler(ask_for_input(TYPING_LAST_NAME)),
        ],
        TYPING_LAST_NAME: [
            make_text_handler(ask_for_input(TYPING_AGE)),
        ],
        TYPING_AGE: [
            make_text_handler(ask_for_input(TYPING_TEST_SCORE)),
        ],
        TYPING_TEST_SCORE: [
            make_message_handler(BTN_I_DONT_KNOW, go_to_test),
            make_text_handler(ask_for_input(TYPING_MEETING_FORMAT)),
        ],
        TYPING_MEETING_FORMAT: [
            make_message_handler(BTN_MEETING_FORMAT_ONLINE, ask_for_input(TYPING_TIME_SLOT)),
            make_message_handler(BTN_MEETING_FORMAT_OFFLINE, ask_for_input(TYPING_TIME_SLOT)),
        ],
        TYPING_TIME_SLOT: [
            make_text_handler(ask_for_input(TYPING_MEETING_CONFIRM)),
        ],
        TYPING_MEETING_CONFIRM: [
            make_message_handler(BTN_CONFIRM_MEETING, process_meeting_confirm(True)),
            make_message_handler(BTN_NOT_CONFIRM_MEETING, process_meeting_confirm(False)),
        ],
    },
    fallbacks=[
        # make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        # make_message_handler(BTN_TESTS_MENU, menu_tests),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.END,
    },
)
