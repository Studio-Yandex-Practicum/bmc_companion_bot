# import json
from unittest import TestCase, mock

import pytest
from httpx import HTTPStatusError, RequestError
from src.request.clients import (  # APIClientResponseError,; APIClientValidationError,
    APIClientRequestError,
    TestAPIClient,
)
from src.schemas.requests import (
    UserSpecificRequest,
    UserTestQuestionAnswerSpecificRequest,
    UserTestSpecificRequest,
)

test_client = TestAPIClient()

breaking_request_user = UserSpecificRequest(user_id=500)
breaking_request_user_test = UserTestSpecificRequest(user_id=500, test_id=1)
breaking_request_user_q_a_test = UserTestQuestionAnswerSpecificRequest(
    user_id=500, test_id=1, test_question_id=1, answer_id=1
)

print("===dict===", breaking_request_user_test.dict())


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

    print(kwargs["params"])
    params = kwargs["params"]

    if params["user_id"] == 500:
        raise RequestError("error", request=FakeRequest(url=kwargs["url"]))

    return MockResponse(None, 400)


@mock.patch("src.request.clients.httpx.request", side_effect=mocked_httpx_request)
class TestTestAPIClient(TestCase):
    def test_request_error_catch(self, mock_request):
        with pytest.raises(APIClientRequestError):
            test_client.all_test_statuses(breaking_request_user_test)
        with pytest.raises(APIClientRequestError):
            test_client.test_result(breaking_request_user_test)
        with pytest.raises(APIClientRequestError):
            test_client.next_question(breaking_request_user_test)
        with pytest.raises(APIClientRequestError):
            test_client.submit_answer(breaking_request_user_q_a_test)
