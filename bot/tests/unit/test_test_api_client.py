from unittest import TestCase, mock

import pytest
from httpx import HTTPStatusError, RequestError
from pydantic import BaseModel
from src.core.constants import APIVersion, Endpoint
from src.request.clients import (
    APIClientRequestError,
    APIClientResponseError,
    APIClientValidationError,
    TestAPIClient,
)
from src.schemas.requests import (
    UserSpecificRequest,
    UserTestQuestionAnswerSpecificRequest,
    UserTestQuestionSpecificRequest,
    UserTestSpecificRequest,
)
from src.schemas.responses import QuestionResponse


class WrongModel(BaseModel):
    wrong_field: str


test_client = TestAPIClient(APIVersion.V1)

breaking_request_u = UserSpecificRequest(user_id=500)
breaking_request_ut = UserTestSpecificRequest(user_id=500, test_id=1)
breaking_request_utq = UserTestQuestionSpecificRequest(user_id=500, test_id=1, test_question_id=1)
breaking_request_utqa = UserTestQuestionAnswerSpecificRequest(
    user_id=500, test_id=1, test_question_id=1, answer_id=1
)
notfound_request_u = UserSpecificRequest(user_id=404)
notfound_request_ut = UserTestSpecificRequest(user_id=404, test_id=1)
notfound_request_utq = UserTestQuestionSpecificRequest(user_id=404, test_id=1, test_question_id=1)
notfound_request_utqa = UserTestQuestionAnswerSpecificRequest(
    user_id=404, test_id=1, test_question_id=1, answer_id=1
)
wrongmodel_request_u = UserSpecificRequest(user_id=418)
wrongmodel_request_ut = UserTestSpecificRequest(user_id=418, test_id=1)
wrongmodel_request_utq = UserTestQuestionSpecificRequest(user_id=418, test_id=1, test_question_id=1)
wrongmodel_request_utqa = UserTestQuestionAnswerSpecificRequest(
    user_id=418, test_id=1, test_question_id=1, answer_id=1
)

correct_next_question_data = {
    "user_id": 1,
    "test_id": 1,
    "test_question_id": 1,
    "text": "Текст вопроса",
    "answers": [{"answer_id": 1, "text": "Да"}, {"answer_id": 2, "text": "Нет"}],
}


def mocked_httpx_request(*args, **kwargs):
    """Имитация ответа httpx.request для тестирования src.request.clients.TestAPIClient."""

    class FakeRequest:
        """Фиктивный запрос с полем url."""

        def __init__(self, url):
            self.url = url

    class MockResponse:
        """Фиктивный HTTP-ответ c полями status_code и json_data, поддерживающий методы json() и
        raise_for_status()."""

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code // 100 in [4, 5]:
                raise HTTPStatusError(
                    "error", response=self, request=FakeRequest(url=kwargs["url"])
                )

    url = kwargs["url"]
    params = kwargs["params"]

    if params["user_id"] == 500:
        raise RequestError("error", request=FakeRequest(url=kwargs["url"]))

    if params["user_id"] == 404:
        return MockResponse({"error": "not found"}, 404)

    if params["user_id"] == 418:
        return MockResponse(WrongModel(wrong_field="Ooops"), 200)

    if url.strip("/").split("/")[-1] == Endpoint.NEXT_QUESTION.split("/")[-1]:
        return MockResponse(QuestionResponse(**correct_next_question_data).dict(), 200)

    return MockResponse(None, 400)


@mock.patch("src.request.clients.httpx.request", side_effect=mocked_httpx_request)
class TestTestAPIClient(TestCase):
    def test_request_error_catch(self, mock_request):
        with pytest.raises(APIClientRequestError):
            test_client.all_test_statuses(breaking_request_u)
        with pytest.raises(APIClientRequestError):
            test_client.test_result(breaking_request_ut)
        with pytest.raises(APIClientRequestError):
            test_client.next_question(breaking_request_ut)
        with pytest.raises(APIClientRequestError):
            test_client.check_answer(breaking_request_utq)
        with pytest.raises(APIClientRequestError):
            test_client.submit_answer(breaking_request_utqa)

    def test_404_catch(self, mock_request):
        with pytest.raises(APIClientResponseError):
            test_client.all_test_results(notfound_request_u)
        with pytest.raises(APIClientResponseError):
            test_client.test_result(notfound_request_ut)
        with pytest.raises(APIClientResponseError):
            test_client.next_question(notfound_request_ut)
        with pytest.raises(APIClientResponseError):
            test_client.check_answer(notfound_request_utq)
        with pytest.raises(APIClientResponseError):
            test_client.submit_answer(notfound_request_utqa)

    def test_validation_error_catch(self, mock_request):
        with pytest.raises(APIClientValidationError):
            test_client.all_test_results(wrongmodel_request_u)
        with pytest.raises(APIClientValidationError):
            test_client.test_result(wrongmodel_request_ut)
        with pytest.raises(APIClientValidationError):
            test_client.next_question(wrongmodel_request_ut)
        with pytest.raises(APIClientValidationError):
            test_client.check_answer(wrongmodel_request_utq)
        with pytest.raises(APIClientValidationError):
            test_client.submit_answer(wrongmodel_request_utqa)

    def test_next_question(self, mock_request):
        response = test_client.next_question(UserTestSpecificRequest(user_id=1, test_id=1))
        assert type(response).__name__.split(".")[-1] == QuestionResponse.__name__.split(".")[-1]
