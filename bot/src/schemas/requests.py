from pydantic import BaseModel


class UserSpecificRequest(BaseModel):
    """Схема запроса к API, требующего указания id пользователя."""

    user_id: int


class UserTestSpecificRequest(UserSpecificRequest):
    """Схема запроса к API, требующего указания id пользователя и теста."""

    test_id: int


class UserTestQuestionSpecificRequest(UserTestSpecificRequest):
    """Схема запроса к API, требующего указания id пользователя, теста и вопроса."""

    test_question_id: int


class UserTestQuestionAnswerSpecificRequest(UserTestQuestionSpecificRequest):
    """Схема запроса к API, требующего указания id пользователя, теста, вопроса и ответа."""

    answer_id: int
