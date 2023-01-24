from typing import TypeVar

from core.constants import APIVersion
from core.settings import settings
from pydantic import BaseModel
from request.exceptions import NoNextQuestion
from schemas.requests import (
    UserIdRequestFromTelegram,
    UserSpecificRequest,
    UserTestQuestionAnswerSpecificRequest,
    UserTestQuestionSpecificRequest,
    UserTestSpecificRequest,
)
from schemas.responses import (
    AllTestResultsResponse,
    AllTestStatusesResponse,
    AnswerInfo,
    AnswerInfoList,
    CheckAnswerResponse,
    QuestionResponse,
    SubmitAnswerResponse,
    TestResultResponse,
    UserIdResponse,
)

from .mock_tests import MOCK_TEST_1, MOCK_TEST_2

WEB_API_URL = f"{settings.APP_HOST}:{settings.APP_PORT}"

ModelType = TypeVar("ModelType", bound=BaseModel)


TESTS = {MOCK_TEST_1["id"]: MOCK_TEST_1, MOCK_TEST_2["id"]: MOCK_TEST_2}
test_positions = {MOCK_TEST_1["id"]: 0, MOCK_TEST_2["id"]: 0}
test_results = {MOCK_TEST_1["id"]: 0, MOCK_TEST_2["id"]: 0}


class MockTestAPIClient:
    """Имитация API-клиента."""

    def __init__(self, api_version: APIVersion) -> None:
        self._base_url = f"http://{WEB_API_URL}/api{api_version}"
        self._question_count = 0
        self._question_number = 3
        self.avalaible = set((MOCK_TEST_1["id"], MOCK_TEST_2["id"]))
        self.active = set()
        self.completed = set()

    def user_id_from_chat_id(self, request: UserIdRequestFromTelegram) -> UserIdResponse:
        """Получение user_id по chat_id."""
        return UserIdResponse(user_id=123)

    def all_test_statuses(self, request: UserSpecificRequest) -> AllTestStatusesResponse:
        """Запрос статуса всех тестов для данного пользователя."""
        available = [
            {"test_id": test_id, "name": TESTS[test_id]["name"]} for test_id in self.avalaible
        ]
        active = [{"test_id": test_id, "name": TESTS[test_id]["name"]} for test_id in self.active]
        completed = [
            {"test_id": test_id, "name": TESTS[test_id]["name"]} for test_id in self.completed
        ]
        return AllTestStatusesResponse(
            user_id=123, available=available, active=active, completed=completed
        )

    # def test_status(self, request: UserTestSpecificRequest) -> TestStatusResponse:
    #     """Запрос статуса конкретного теста для данного пользователя."""
    #     url = urljoin(self._base_url, Endpoint.TEST_STATUS)
    #     response = self._safe_request(HTTPMethod.GET, url=url, params=request.dict())
    #     return self._process_response(response, TestStatusResponse)

    def next_question(self, request: UserTestSpecificRequest) -> QuestionResponse:
        if request.test_id in self.avalaible:
            self.avalaible.remove(request.test_id)
            self.active.add(request.test_id)
        test_id = request.test_id
        if test_positions[test_id] == len(TESTS[test_id]["questions"]):
            self.active.remove(test_id)
            self.completed.add(test_id)
            raise NoNextQuestion
        answers_list = TESTS[test_id]["questions"][test_positions[test_id]]["answers"]
        answers = [
            AnswerInfo(answer_id=answer["id"], text=answer["text"]) for answer in answers_list
        ]
        answers = AnswerInfoList(__root__=answers)
        return QuestionResponse(
            user_id=123,
            test_id=test_id,
            test_question_id=TESTS[test_id]["questions"][test_positions[test_id]]["id"],
            text=TESTS[test_id]["questions"][test_positions[test_id]]["text"],
            answers=answers,
        )

    def submit_answer(self, request: UserTestQuestionAnswerSpecificRequest) -> SubmitAnswerResponse:
        """Передача ответа на вопрос в тесте от имени пользователя."""
        test_id = request.test_id
        answer_id = request.answer_id
        question = TESTS[test_id]["questions"][test_positions[test_id]]
        for answer in question["answers"]:
            if answer["id"] == answer_id:
                test_results[test_id] += answer["value"]
        test_positions[test_id] += 1
        return None

    def test_result(self, request: UserTestSpecificRequest) -> TestResultResponse:
        """Запрос результата данного теста для данного пользователя."""
        test_id = request.test_id
        name = TESTS[test_id]["name"]
        value = test_results[test_id]

        return TestResultResponse(test_id=1, name=name, value=value, user_id=123)

    def all_test_results(self, request: UserSpecificRequest) -> AllTestResultsResponse:
        """Запрос результатов всех тестов для данного пользователя."""
        # url = urljoin(self._base_url, Endpoint.ALL_TEST_RESULTS)
        # response = self._safe_request(HTTPMethod.GET, url=url, params=request.dict())
        # return self._process_response(response, AllTestResultsResponse)
        pass

    def check_answer(self, request: UserTestQuestionSpecificRequest) -> CheckAnswerResponse:
        """Запрос ранее полученного ответа на данный вопрос данного теста
        от имени данного пользователя."""
        # url = urljoin(self._base_url, Endpoint.CHECK_ANSWER)
        # response = self._safe_request(HTTPMethod.GET, url=url, params=request.dict())
        # return self._process_response(response, CheckAnswerResponse)
        pass
