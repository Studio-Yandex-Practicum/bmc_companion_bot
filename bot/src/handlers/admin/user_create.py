from handlers.admin.user_entrypoint import (
    CREATING_NEW_USER,
    MENU_USERS_SELECTING_LEVEL,
    TYPING_USER_LOGIN_FOR_CREATE_USER,
    TYPING_USER_LOGIN_FOR_DELETE_USER,
    USER_CREATE_CLIENT,
    main_users_list,
)
from schemas.requests import UserCreateRequest
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_ADMIN_MENU

SCRIPT_CREATING_NEW_USER, SCRIPT_DELETE_USER = range(2)


async def ask_for_input_user_fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_data["login"] = update.message.text
    if not user_data.get("login").isnumeric():
        text = "Логин некорректен, попробуйте снова"
        await update.message.reply_text(text=text)
        await main_users_list(update, context)
        return MENU_USERS_SELECTING_LEVEL
    text = f"Введите имя психолога с логином {user_data['login']}:"
    await update.message.reply_text(text=text)
    return CREATING_NEW_USER


def ask_for_input_user_login(script: int = SCRIPT_DELETE_USER):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = "Введите логин психолога:"

        if script == SCRIPT_CREATING_NEW_USER:
            buttons = [
                [
                    BTN_ADMIN_MENU,
                ],
            ]
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
            await update.message.reply_text(text=text, reply_markup=keyboard)
            return TYPING_USER_LOGIN_FOR_CREATE_USER
        await update.message.reply_text(text=text)
        return TYPING_USER_LOGIN_FOR_DELETE_USER

    return inner


async def create_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_data["user_fio"] = update.message.text
    input = user_data.get("user_fio").split()

    if len(input) == 3 and all([str(i).isalpha() for i in input]):
        last_name, first_name, middle_name = input
        text = (
            f"Психолог \nlogin: {user_data['login']}\n"
            f"first name: {first_name}\n"
            f"last name: {last_name}\n"
            f"middle name: {middle_name}\n"
        )
    else:
        text = "ФИО некорректно, попробуйте снова"
        await update.message.reply_text(text=text)
        await main_users_list(update, context)
        return MENU_USERS_SELECTING_LEVEL

    user_role_id = 1  # Не нашел константу, пока единичка

    user = USER_CREATE_CLIENT.create(
        UserCreateRequest(
            role_id=user_role_id,
            telegram_id=user_data.get("login"),
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
        )
    )
    user = True
    if user:
        text += "успешно создан"
    else:
        text += "уже существует"

    await update.message.reply_text(text=text)

    await main_users_list(update, context)

    return MENU_USERS_SELECTING_LEVEL
