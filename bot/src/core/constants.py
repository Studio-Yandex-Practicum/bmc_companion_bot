from enum import Enum


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


MOCK_TEST_1 = {
    "test_id": 1,
    "name": "Первый тест",
    "questions": [
        {
            "question_id": 11,
            "text": "Текст первого вопроса",
            "answers": [
                {"text": "Да", "value": 1},
                {"text": "Нет", "value": 0},
            ],
        },
        {
            "question_id": 12,
            "text": "Текст второго вопроса",
            "answers": [
                {"text": "Да", "value": 1},
                {"text": "Нет", "value": 0},
            ],
        },
    ],
}

MOCK_TEST_2 = {
    "test_id": 1,
    "name": "Тест второй",
    "questions": [
        {
            "question_id": 11,
            "text": "Текст первого вопроса",
            "answers": [
                {"text": "Да", "value": 1},
                {"text": "Нет", "value": 0},
            ],
        },
        {
            "question_id": 12,
            "text": "Текст второго вопроса",
            "answers": [
                {"text": "Да", "value": 1},
                {"text": "Нет", "value": 0},
            ],
        },
    ],
}


MOCK_TESTS = [MOCK_TEST_1, MOCK_TEST_2]
