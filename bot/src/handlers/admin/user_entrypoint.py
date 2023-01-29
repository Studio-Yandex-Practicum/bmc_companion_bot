from core.constants import APIVersion, Endpoint
from request.clients import ObjAPIClient
from schemas.requests import BaseModel, UserSpecificRequest
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from ui.buttons import BTN_ADD_USER, BTN_ADMIN_MENU, BTN_DELETE_USER, BTN_SHOW_USERS

MENU_USERS_SELECTING_LEVEL = "MENU_USERS_SELECTING_LEVEL"
TYPING_USER_LOGIN_FOR_CREATE_USER = "TYPING_USER_LOGIN_FOR_CREATE_USER"
TYPING_USER_FIO_FOR_CREATE_USER = "TYPING_USER_FIO_FOR_CREATE_USER"
TYPING_USER_LOGIN_FOR_DELETE_USER = "TYPING_USER_ID_FOR_DELETE_USER"
TYPING_CONFIRM_FOR_DELETE_USER = "TYPING_CONFIRM_FOR_DELETE_USER"

CREATING_NEW_USER = "CREATING_NEW_USER"

USER_CREATE_CLIENT = ObjAPIClient(
    api_version=APIVersion.V1,
    endpoint=Endpoint.USERS,
    model=[BaseModel],
    many_model=[BaseModel],
)

USER_DELETE_CLIENT = ObjAPIClient(
    api_version=APIVersion.V1,
    endpoint=Endpoint.USERS,
    model=[UserSpecificRequest],
    many_model=[BaseModel],
)

USER_GET_CLIENT = USER_DELETE_CLIENT


async def main_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = "Раздел редактирования психологов"
    buttons = [
        [
            BTN_SHOW_USERS,
            BTN_ADD_USER,
            BTN_DELETE_USER,
        ],
        [
            BTN_ADMIN_MENU,
        ],
    ]
    keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

    await update.message.reply_text(text, reply_markup=keyboard)

    return MENU_USERS_SELECTING_LEVEL
