from enum import Enum

from telegram.ext import ConversationHandler


class Endpoint(str, Enum):
    MEETINGS = "api/v1/meetings"
    TESTS = "api/v1/tests"


class HTTPMethod(str, Enum):
    CONNECT = "CONNECT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    GET = "GET"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


class BotState(str, Enum):
    MENU_START_SELECTING_LEVEL = "MENU_START_SELECTING_LEVEL"
    MENU_ADMIN_SELECTING_LEVEL = "MENU_ADMIN_SELECTING_LEVEL"
    STOPPING = "STOPPING"
    END = ConversationHandler.END
