from dataclasses import dataclass

from request.exceptions import NoNextQuestion
from request.services import PydanticApiService
from schemas.responses import (
    AllTestStatusesResponse,
    QuestionResponse,
    SubmitAnswerResponse,
    TestResultResponse,
    UceTestResponse,
)


@dataclass
class QuestioningApiService(PydanticApiService):
    URL_UCE_TEST = "uce_test"
    URL_NEXT_QUESTION = "next_question"
    URL_SUBMIT_ANSWER = "submit_answer"
    URL_ALL_TEST_STATUSES = "test_statuses/all"
    URL_TEST_RESULT = "test_results"

    def all_test_statuses(self, **kwargs) -> AllTestStatusesResponse:
        """Запрос статуса всех тестов для данного пользователя."""
        return self.get(AllTestStatusesResponse, self.URL_ALL_TEST_STATUSES, params={**kwargs})

    def next_question(self, **kwargs) -> QuestionResponse:
        """Запрос следующего вопроса для данного пользователя в данном тесте."""
        question = self.get(QuestionResponse, self.URL_NEXT_QUESTION, params={**kwargs})
        if not question:
            raise NoNextQuestion
        return question

    def submit_answer(
        self, user_id: int, test_id: int, question_id: int, answer_id: int
    ) -> SubmitAnswerResponse:
        """Передача ответа на вопрос в тесте от имени пользователя."""
        data = {
            "user_id": user_id,
            "test_id": test_id,
            "question_id": question_id,
            "answer_id": answer_id,
        }
        return self.post(SubmitAnswerResponse, self.URL_SUBMIT_ANSWER, data)

    def test_result(self, **kwargs) -> TestResultResponse:
        """Запрос результата данного теста для данного пользователя."""
        return self.get(TestResultResponse, self.URL_TEST_RESULT, params={**kwargs})

    def uce_test_id(self, **kwargs) -> UceTestResponse:
        return self.get(UceTestResponse, self.URL_UCE_TEST, params={**kwargs})
