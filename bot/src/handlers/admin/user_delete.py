from handlers.admin.user_entrypoint import (
    MENU_USERS_SELECTING_LEVEL,
    TYPING_CONFIRM_FOR_DELETE_USER,
    TYPING_USER_LOGIN_FOR_DELETE_USER,
    USER_DELETE_CLIENT,
    main_users_list,
)
from telegram import Update
from telegram.ext import ContextTypes

SCRIPT_CREATING_NEW_USER, SCRIPT_DELETE_USER = range(2)


def ask_for_input_user_login(script: int = SCRIPT_DELETE_USER):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = "Введите логин психолога:"
        await update.message.reply_text(text=text)
        return TYPING_USER_LOGIN_FOR_DELETE_USER

    return inner


async def ask_confirmation_for_user_deletion(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    user_data = context.user_data
    user_data["login"] = update.message.text
    if not user_data.get("login").isnumeric():
        text = "Логин некорректен, попробуйте снова"
        await update.message.reply_text(text=text)
        await main_users_list(update, context)
        return MENU_USERS_SELECTING_LEVEL
    # Получение списка юзеров
    users = USER_DELETE_CLIENT.get()
    user_to_delete = None
    # Получение юзера по логину
    for user in users:
        if user.telegram_id == user_data.get("login"):
            user_to_delete = user
    if user_to_delete is not None:
        user_data["user_to_delete"] = user_to_delete
        text = f"Вы точно хотите удалить психолога {user_to_delete}? (y/n)"
        await update.message.reply_text(text=text)
        return TYPING_CONFIRM_FOR_DELETE_USER

    text = f"Психолог с логином {user_data.get('login')} не найден"
    await update.message.reply_text(text=text)

    await main_users_list(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_to_delete = user_data["user_to_delete"]
    confirm_deletion = update.message.text

    if confirm_deletion.lower() == "y":

        USER_DELETE_CLIENT.delete(id=user_to_delete.id)

        text = f"Психолог {user_to_delete} удален!"
    else:
        text = f"Психолог {user_to_delete} остался без изменений. Он не удален!"

    await update.message.reply_text(text=text)

    await main_users_list(update, context)

    return MENU_USERS_SELECTING_LEVEL
