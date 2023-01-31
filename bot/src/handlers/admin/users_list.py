# from webapi.src.app import db

from core.constants import BotState
from handlers.admin.root_handlers import back_to_admin
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import (
    BTN_ADD_TIMESLOT,
    BTN_ADD_USER,
    BTN_ADMIN_MENU,
    BTN_DELETE_TIMESLOT,
    BTN_DELETE_USER,
    BTN_PSYCHOLOGISTS_LIST,
    BTN_SCHEDULE,
    BTN_SHOW_USERS,
)
from utils import demo_api_client, make_message_handler, make_text_handler

MENU_USERS_SELECTING_LEVEL = "MENU_USERS_SELECTING_LEVEL"
MENU_USERS_LIST_SELECTING_LEVEL = "MENU_USERS_LIST_SELECTING_LEVEL"
TYPING_TG_LOGIN_FOR_DELETE_USER = "TYPING_TG_LOGIN_FOR_DELETE_USER"
TYPING_CONFIRM_FOR_DELETE_USER = "TYPING_CONFIRM_FOR_DELETE_USER"
TYPING_TG_ID_FOR_ADD_NEW_USER = "TYPING_TG_ID_FOR_ADD_NEW_USER"
TYPING_TG_LOGIN_FOR_CHANGE_SCHEDULE = "TYPING_TG_LOGIN_FOR_CHANGE_SCHEDULE"
MENU_SCHEDULE_SELECTING_LEVEL = "MENU_SCHEDULE_SELECTING_LEVEL"

CREATING_NEW_USER = "CREATING_NEW_USER"
CREATING_NEW_TIMESLOT = "CREATING_NEW_TIMESLOT"

SCRIPT_ADD_USER, SCRIPT_DELETE_USER, SCRIPT_SCHEDULE = range(3)


async def menu_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Раздел редактирования психологов"
    buttons = [
        [BTN_SHOW_USERS, BTN_ADD_USER],
        [BTN_ADMIN_MENU],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=keyboard)

    return MENU_USERS_SELECTING_LEVEL


async def menu_admins_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Список психологов:\n"

    users = demo_api_client.get_users()
    for index, user in enumerate(users):
        if not user["deleted_at"]:
            text += f"\n{index + 1}. {user['first_name']} ({user['telegram_login']})"

    context.user_data["users"] = users

    buttons = [
        [BTN_ADD_USER, BTN_DELETE_USER, BTN_SCHEDULE],
        [BTN_PSYCHOLOGISTS_LIST],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=keyboard)

    return MENU_USERS_LIST_SELECTING_LEVEL


async def menu_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    tg_login = update.message.text

    user = demo_api_client.get_user_by_tg_login(tg_login)

    if user:
        user_data["tg_login"] = tg_login
        text = f"Расписание психолога {user.get('first_name')}:\n"

        items = demo_api_client.get_timeslots(tg_login)
        for index, item in enumerate(items):
            if not item["deleted_at"]:
                text += f"\n{index + 1}. {item['first_name']} ({user['telegram_login']})"

        buttons = [
            [BTN_ADD_TIMESLOT, BTN_DELETE_TIMESLOT],
            [BTN_PSYCHOLOGISTS_LIST],
        ]
        keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

        await update.message.reply_text(text, reply_markup=keyboard)

        return MENU_SCHEDULE_SELECTING_LEVEL

    text = f"Юзера с логином {tg_login} не существует"
    await update.message.reply_text(text=text)

    await menu_users(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def ask_for_input_new_timeslot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    tg_login = user_data["tg_login"]

    user = demo_api_client.get_user_by_tg_login(tg_login)

    if user:
        text = "Введите новый таймслот в формате DD MM GG HH MM:"
        await update.message.reply_text(text=text)
        return CREATING_NEW_TIMESLOT

    text = f"Юзер с логином {tg_login} не существует"
    await update.message.reply_text(text=text)

    await menu_users(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def create_new_timeslot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    tg_login = user_data["tg_login"]
    timeslot = update.message.text

    demo_api_client.create_timeslot(tg_login, timeslot)
    text = "Новый таймслот успешно добавлен!"

    await update.message.reply_text(text=text)

    await menu_users(update, context)

    return MENU_USERS_SELECTING_LEVEL


def ask_for_input_user_id(script: int = SCRIPT_ADD_USER):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = "Введите TG логин психолога:"

        await update.message.reply_text(text=text)

        if script == SCRIPT_DELETE_USER:
            return TYPING_TG_LOGIN_FOR_DELETE_USER
        elif script == SCRIPT_SCHEDULE:
            return TYPING_TG_LOGIN_FOR_CHANGE_SCHEDULE

        return TYPING_TG_ID_FOR_ADD_NEW_USER

    return inner


async def ask_for_input_user_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    tg_login = update.message.text

    user = demo_api_client.get_user_by_tg_login(tg_login)

    if not user:
        user_data["tg_login"] = tg_login
        text = "Введите имя нового психолога:"
        await update.message.reply_text(text=text)
        return CREATING_NEW_USER

    text = f"Юзер с логином {tg_login} уже существует"
    await update.message.reply_text(text=text)

    await menu_users(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def create_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_name = update.message.text
    tg_login = user_data["tg_login"]

    demo_api_client.create_user({"telegram_login": tg_login, "first_name": user_name, "role_id": 3})
    text = "Новый психолог успешно добавлен!"

    await update.message.reply_text(text=text)

    await menu_users(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def ask_confirmation_for_user_deletion(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    user_data = context.user_data
    tg_login = update.message.text

    user = demo_api_client.get_user_by_tg_login(tg_login)

    if user:
        user_data["user_id"] = int(user["id"])
        text = "Вы точно хотите удалить психолога? (y/n)"
        await update.message.reply_text(text=text)
        return TYPING_CONFIRM_FOR_DELETE_USER

    text = f"Юзер с логином {tg_login} не найден среди психологов"
    await update.message.reply_text(text=text)

    await menu_users(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_id = user_data["user_id"]
    confirm_deletion = update.message.text

    if confirm_deletion.lower() == "y":
        demo_api_client.delete_user_by_id(int(user_id))
        text = "Психолог удален!"
    else:
        text = "Психолог остался без изменений. Он не удален!"

    await update.message.reply_text(text=text)

    await menu_users(update, context)

    return MENU_USERS_SELECTING_LEVEL


users_list_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_PSYCHOLOGISTS_LIST, menu_users),
    ],
    states={
        MENU_USERS_SELECTING_LEVEL: [
            make_message_handler(BTN_SHOW_USERS, menu_admins_list),
            make_message_handler(BTN_ADD_USER, ask_for_input_user_id(SCRIPT_ADD_USER)),
        ],
        MENU_USERS_LIST_SELECTING_LEVEL: [
            make_message_handler(BTN_ADD_USER, ask_for_input_user_id(SCRIPT_ADD_USER)),
            make_message_handler(BTN_DELETE_USER, ask_for_input_user_id(SCRIPT_DELETE_USER)),
            make_message_handler(BTN_SCHEDULE, ask_for_input_user_id(SCRIPT_SCHEDULE)),
        ],
        TYPING_TG_ID_FOR_ADD_NEW_USER: [
            make_text_handler(ask_for_input_user_name),
        ],
        CREATING_NEW_USER: [
            make_text_handler(create_new_user),
        ],
        TYPING_TG_LOGIN_FOR_DELETE_USER: [
            make_text_handler(ask_confirmation_for_user_deletion),
        ],
        TYPING_CONFIRM_FOR_DELETE_USER: [
            make_text_handler(delete_user),
        ],
        TYPING_TG_LOGIN_FOR_CHANGE_SCHEDULE: [
            make_text_handler(menu_schedule),
        ],
        MENU_SCHEDULE_SELECTING_LEVEL: [
            make_message_handler(BTN_ADD_TIMESLOT, ask_for_input_new_timeslot),
        ],
        CREATING_NEW_TIMESLOT: [
            make_text_handler(create_new_timeslot),
        ],
    },
    fallbacks=[
        make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        make_message_handler(BTN_PSYCHOLOGISTS_LIST, menu_users),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.MENU_ADMIN_SELECTING_LEVEL,
    },
)
