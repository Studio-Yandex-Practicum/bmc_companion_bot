from core.constants import APIVersion, BotState, Endpoint
from handlers.admin.root_handlers import back_to_admin
from handlers.admin.user_create import (
    ask_for_input_user_fio,
    ask_for_input_user_login,
    create_new_user,
)
from handlers.admin.user_delete import ask_confirmation_for_user_deletion, delete_user
from handlers.admin.user_entrypoint import main_users_list
from request.clients import ObjAPIClient
from schemas.requests import BaseModel, UserCreateRequest
from telegram.ext import ConversationHandler
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
    model=[UserCreateRequest],
    many_model=[BaseModel],
)

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
