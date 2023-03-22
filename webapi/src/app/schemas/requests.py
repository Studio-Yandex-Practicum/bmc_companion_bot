from pydantic import BaseModel


class UserIdRequestFromTelegram(BaseModel):
    """Модель запроса user_id по chat_id Телеграма."""

    chat_id: int


class AllTestResultsRequest(BaseModel):
    """Модель запроса для получения результатов всех тестов данного юзера."""

    user_id: int


class TestResultRequest(AllTestResultsRequest):
    """Модель запроса для получения результата конкретного теста данного юзера."""

    test_id: int


class AllTestStatusesRequest(AllTestResultsRequest):
    """Модель запроса статуса всех тестов для данного юзера."""

    pass


class TestStatusRequest(TestResultRequest):
    """Модель запроса статуса конкретного теста для данного юзера."""

    pass


class NextQuestionRequest(TestResultRequest):
    """Модель запроса следующего вопроса для указанного юзера из указанного теста."""

    pass


class CheckAnswerRequest(TestResultRequest):
    """Модель запроса ответа, ранее данного указанным юзером на указанный вопрос теста."""

    test_question_id: int


class SubmitAnswerRequest(CheckAnswerRequest):
    """Модель передачи ответа на указаный вопрос."""

    answer_id: int
