from enum import Enum


class Endpoint(str, Enum):
    MEETINGS = "api/v1/meetings"
    TESTS = "api/v1/tests"
    NEXT_QUESTION = "api/v1/next_question"
    SUBMIT_ANSWER = "api/v1/submit_answer"
    TEST_STATUS = "/api/v1/test_statuses"
    ALL_TEST_STATUSES = "/api/v1/test_statuses/all"
    TEST_RESULT = "/api/v1/test_results"
    ALL_TEST_RESULTS = "/api/v1/test_results/all/"
    CHECK_ANSWER = "/api/v1/check_answer"


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
