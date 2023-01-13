from typing import List

from core.constants import TestStatus
from pydantic import BaseModel


class TestInfo(BaseModel):
    """Модель информации о тесте."""

    test_id: int
    name: str


class TestInfoList(BaseModel):
    """Модель списка информации о тестах."""

    __root__: List[TestInfo]


class TestResult(TestInfo):
    """Модель информации о результате теста."""

    value: int


class TestResultList(BaseModel):
    """Модель списка результатов теста."""

    __root__: List[TestResult]


class TestResultResponse(TestResult):
    """Модель ответа с результатом конкретного теста для данного юзера."""

    user_id: int


class AllTestResultsResponse(BaseModel):
    """Модель ответа с результатом конкретного теста для данного юзера."""

    user_id: int
    results: TestResultList


class TestStatusResponse(TestInfo):
    """Модель ответа с инфорамацией о статусе конкретного теста для данного юзера."""

    user_id: int
    status: TestStatus


class AllTestStatusesResponse(BaseModel):
    """Модель ответа с инфорамацией о статусе всех тестов для данного юзера."""

    user_id: int
    available: TestInfoList
    active: TestInfoList
    completed: TestInfoList


class AnswerInfo(BaseModel):
    """Модель информации об ответе на вопрос теста."""

    answer_id: int
    text: str


class AnswerInfoList(BaseModel):
    """Модель cписка информации об ответе на вопрос теста."""

    __root__: List[AnswerInfo]


class QuestionInfo(BaseModel):
    """Модель информации о вопросе."""

    test_question_id: int
    text: str
    answers: AnswerInfoList


class QuestionResponse(QuestionInfo):
    """Модель ответа на запрос следующего вопроса указанного теста для указанного юзера."""

    user_id: int
    test_id: int


class SubmitAnswerResponse(BaseModel):
    """Модель ответа на POST-запрос внесения ответа на вопрос теста."""

    user_id: int
    test_id: int
    test_question_id: int
    answer_id: int


class CheckAnswerResponse(SubmitAnswerResponse):
    """Модель ответа на запрос ответа, данного указанным юзером на указанный вопрос теста."""

    text: str
    value: int
