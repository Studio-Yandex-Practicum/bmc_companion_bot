from pydantic import BaseModel


class UserIdRequestFromTelegram(BaseModel):
    """Модель запроса user_id по chat_id Телеграма."""

    chat_id: int


class UserSpecificRequest(BaseModel):
    """Схема запроса к API, требующего указания id пользователя."""

    user_id: int


class UserTestSpecificRequest(UserSpecificRequest):
    """Схема запроса к API, требующего указания id пользователя и теста."""

    test_id: int


class UserTestQuestionSpecificRequest(UserTestSpecificRequest):
    """Схема запроса к API, требующего указания id пользователя, теста и вопроса."""

    question_id: int


class UserTestQuestionAnswerSpecificRequest(UserTestQuestionSpecificRequest):
    """Схема запроса к API, требующего указания id пользователя, теста, вопроса и ответа."""

    answer_id: int


class UceTestRequest(BaseModel):
    """Модель запроса test_id по test_name"""

    pass
