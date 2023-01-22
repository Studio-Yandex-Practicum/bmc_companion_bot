from enum import Enum

from telegram.ext import ConversationHandler


class APIVersion(str, Enum):
    V1 = "/v1"


class Endpoint(str, Enum):
    MEETINGS = "/meetings"
    TESTS = "/tests"
    NEXT_QUESTION = "/next_question"
    SUBMIT_ANSWER = "/submit_answer"
    TEST_STATUS = "/test_statuses"
    ALL_TEST_STATUSES = "/test_statuses/all"
    TEST_RESULT = "/test_results"
    ALL_TEST_RESULTS = "/test_results/all"
    CHECK_ANSWER = "/check_answer"
    USERS = "/users"


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
    STOPPING = "STOPPING"
    END = ConversationHandler.END
