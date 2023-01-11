from pydantic import BaseModel


class AllTestResultsRequest(BaseModel):
    """Модель запроса для получения результатов всех тестов данного юзера."""

    user_id: int


class TestResultRequest(AllTestResultsRequest):
    """Модель запроса для получения результата конкретного теста данного юзера."""

    test_id: int
