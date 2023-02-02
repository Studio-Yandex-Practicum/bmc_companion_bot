from enum import Enum

from telegram.ext import ConversationHandler


class APIVersion(str, Enum):
    V1 = "/v1"


class Endpoint(str, Enum):
    MEETINGS = "/meetings"
    TESTS = "/tests"
    NEXT_QUESTION = "/next_question"
    SUBMIT_ANSWER = "/submit_answer"
    TEST_STATUS = "test_statuses"
    ALL_TEST_STATUSES = "test_statuses/all"
    TEST_RESULT = "test_results"
    ALL_TEST_RESULTS = "test_results/all"
    CHECK_ANSWER = "check_answer"
    USER_ID_FROM_CHAT_ID = "/user_id_from_chat_id"
    USER = "/users"


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


class TestStatus(str, Enum):
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"


class BotState(str, Enum):
    MENU_START_SELECTING_LEVEL = "MENU_START_SELECTING_LEVEL"
    MENU_ADMIN_SELECTING_LEVEL = "MENU_ADMIN_SELECTING_LEVEL"
    MENU_TEST_SELECTING_LEVEL = "MENU_TEST_SELECTING_LEVEL"
    MENU_MEETING_SELECTING_LEVEL = "MENU_MEETING_SELECTING_LEVEL"
    QUESTIONING = "QUESTIONING"
    STOPPING = "STOPPING"
    END = ConversationHandler.END
    ERROR = "ERROR"


class UserRole(int, Enum):
    ROOT = 1
    ADMIN = 2
    USER = 3


RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DO_NOTHING_SIGN = "-"
KEY_RESULTS_FOR_PAGINATED_RESPONSE = "results"
