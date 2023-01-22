from core.constants import APIVersion, BotState, Endpoint
from handlers.admin.root_handlers import back_to_admin
from request.clients import ObjAPIClient
from schemas.requests import BaseModel, UserSpecificRequest
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from ui.buttons import (
    BTN_ADD_USER,
    BTN_ADMIN_MENU,
    BTN_DELETE_USER,
    BTN_PSYCHOLOGISTS_LIST,
    BTN_SHOW_USERS,
)
from utils import make_message_handler, make_text_handler

MENU_USERS_SELECTING_LEVEL = "MENU_USERS_SELECTING_LEVEL"
TYPING_USER_LOGIN_FOR_CREATE_USER = "TYPING_USER_LOGIN_FOR_CREATE_USER"
TYPING_USER_FIO_FOR_CREATE_USER = "TYPING_USER_FIO_FOR_CREATE_USER"
TYPING_USER_LOGIN_FOR_DELETE_USER = "TYPING_USER_ID_FOR_DELETE_USER"
TYPING_CONFIRM_FOR_DELETE_USER = "TYPING_CONFIRM_FOR_DELETE_USER"

CREATING_NEW_USER = "CREATING_NEW_USER"

SCRIPT_CREATING_NEW_USER, SCRIPT_DELETE_USER = range(2)

USER_CREATE_CLIENT = ObjAPIClient(
    api_version=APIVersion.V1,
    endpoint=Endpoint.USERS,
    model=[UserSpecificRequest],
    many_model=[BaseModel],
)


async def main_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Раздел редактирования психологов"
    buttons = [
        [BTN_SHOW_USERS, BTN_ADD_USER],
        [
            BTN_ADMIN_MENU,
            BTN_DELETE_USER,
        ],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=keyboard)

    return MENU_USERS_SELECTING_LEVEL


async def ask_for_input_user_fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_data["login"] = update.message.text
    text = f"Введите имя психолога с логином {user_data['login']}:"
    await update.message.reply_text(text=text)
    return CREATING_NEW_USER


def ask_for_input_user_login(script: int = SCRIPT_DELETE_USER):
    async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        text = "Введите логин психолога:"
        buttons = [
            [
                BTN_ADMIN_MENU,
            ],
        ]
        if script == SCRIPT_CREATING_NEW_USER:
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
            await update.message.reply_text(text=text, reply_markup=keyboard)
            return TYPING_USER_LOGIN_FOR_CREATE_USER
        await update.message.reply_text(text=text)
        return TYPING_USER_LOGIN_FOR_DELETE_USER

    return inner


async def create_new_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_data["user_fio"] = update.message.text
    last_name, first_name, middle_name = user_data.get("user_fio").split()

    # TODO: Как получить id роли "user"?
    # user_role_id = ?

    # TODO: Создать юзера
    # response = USER_CREATE_CLIENT.create(
    #     user_roles=,
    #     last_name=last_name,
    #     first_name=first_name,
    #     middle_name=middle_name
    # )

    user_exists = False
    text = (
        f"Психолог \nlogin: '{user_data['login']}'\n"
        f"first name: '{first_name}'\n"
        f"last name: '{last_name}'\n"
        f"middle name: '{middle_name}'\n"
    )
    if user_exists:
        text += "уже существует"
    else:
        text += "успешно создан"

    await update.message.reply_text(text=text)

    await main_users_list(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def ask_confirmation_for_user_deletion(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    user_data = context.user_data
    user_login = update.message.text

    # TODO: найти user по user_login???

    user = "not_none"
    if user is not None:
        user_data["user_to_delete"] = user
        text = f"Вы точно хотите удалить психолога {user}? (y/n)"
        await update.message.reply_text(text=text)
        return TYPING_CONFIRM_FOR_DELETE_USER

    text = f"Психолог с логином {user_login} не найден"
    await update.message.reply_text(text=text)

    await main_users_list(update, context)

    return MENU_USERS_SELECTING_LEVEL


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user_data = context.user_data
    user_to_delete = user_data["user_to_delete"]
    confirm_deletion = update.message.text

    if confirm_deletion.lower() == "y":

        # TODO: удалить user

        text = f"Психолог {user_to_delete} удален!"
    else:
        text = f"Психолог {user_to_delete} остался без изменений. Он не удален!"

    await update.message.reply_text(text=text)

    await main_users_list(update, context)

    return MENU_USERS_SELECTING_LEVEL


users_list_section = ConversationHandler(
    entry_points=[
        make_message_handler(BTN_PSYCHOLOGISTS_LIST, main_users_list),
    ],
    states={
        MENU_USERS_SELECTING_LEVEL: [
            make_message_handler(BTN_ADD_USER, ask_for_input_user_login(SCRIPT_CREATING_NEW_USER)),
            make_message_handler(BTN_DELETE_USER, ask_for_input_user_login(SCRIPT_DELETE_USER)),
        ],
        CREATING_NEW_USER: [make_text_handler(create_new_user)],
        TYPING_USER_LOGIN_FOR_CREATE_USER: [
            make_text_handler(ask_for_input_user_fio),
            make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        ],
        TYPING_USER_LOGIN_FOR_DELETE_USER: [
            make_text_handler(ask_confirmation_for_user_deletion),
        ],
        TYPING_CONFIRM_FOR_DELETE_USER: [
            make_text_handler(delete_user),
        ],
    },
    fallbacks=[
        make_message_handler(BTN_ADMIN_MENU, back_to_admin),
        make_message_handler(BTN_SHOW_USERS, main_users_list),
    ],
    map_to_parent={
        BotState.STOPPING: BotState.MENU_ADMIN_SELECTING_LEVEL,
    },
)
