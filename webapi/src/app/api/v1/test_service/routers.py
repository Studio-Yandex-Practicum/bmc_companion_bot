from http import HTTPStatus

from app.schemas.requests import (
    AllTestResultsRequest,
    AllTestStatusesRequest,
    CheckAnswerRequest,
    NextQuestionRequest,
    SubmitAnswerRequest,
    TestResultRequest,
    TestStatusRequest,
    UserIdRequestFromTelegram,
)
from app.schemas.responses import (
    AllTestResultsResponse,
    AllTestStatusesResponse,
    CheckAnswerResponse,
    QuestionResponse,
    SubmitAnswerResponse,
    TestResultResponse,
    TestStatusResponse,
    UserIdResponse,
)
from app.services.exceptions import (
    AnswerNotFound,
    NoNextQuestion,
    TestNotFound,
    TestQuestionNotFound,
)
from app.services.test_service import TestService
from app.utils import obj_or_abort_404
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource, reqparse

chat_parser = reqparse.RequestParser()
chat_parser.add_argument("chat_id", type=int, required=True)
user_parser = reqparse.RequestParser()
user_parser.add_argument("user_id", type=int, required=True)
test_parser = user_parser.copy()
test_parser.add_argument("user_id", type=int, required=True)
question_parser = test_parser.copy()
question_parser.add_argument("question_id", type=int, required=True)
answer_parser = question_parser.copy()
answer_parser.add_argument("answer_id", type=int, required=True)


class UserIdFromTelegram(Resource):
    @validate()
    def get(self) -> UserIdResponse:
        """Получение user_id по chat_id Телеграма."""
        user_id = TestService.user_id_from_chat_id(
            UserIdRequestFromTelegram(**chat_parser.parse_args())
        )
        return user_id


class AllTestResults(Resource):
    @validate()
    def get(self) -> AllTestResultsResponse:
        """Получение результатов всех тестов юзера с данным id."""
        test_results = TestService.get_all_test_results(
            AllTestResultsRequest(**user_parser.parse_args())
        )
        return test_results


class TestResult(Resource):
    @validate()
    def get(self) -> TestResultResponse:
        """Получение результата конкретного теста юзера с данным id."""
        return obj_or_abort_404(
            TestService.get_test_result,
            TestResultRequest(**test_parser.parse_args()),
            TestNotFound,
            "Результата теста с заданным id не существует.",
        )


class UCETestResult(Resource):
    @validate()
    def get(self) -> TestResultResponse:
        """Получение результата НДО теста юзера."""
        return obj_or_abort_404(
            TestService.get_uce_score,
            TestResultRequest(**test_parser.parse_args()),
            TestNotFound,
            "Результата теста с заданным id не существует.",
        )


class TestStatus(Resource):
    @validate()
    def get(self) -> TestStatusResponse:
        """Получение статуса конкретного теста для юзера с данным id."""
        return obj_or_abort_404(
            TestService.get_test_status,
            TestStatusRequest(**test_parser.parse_args()),
            TestNotFound,
            "Теста с заданным id не существует.",
        )


class AllTestStatuses(Resource):
    @validate()
    def get(self) -> AllTestStatusesResponse:
        """Получение статуса всех тестов для юзера с даннным id."""
        return TestService.get_all_test_statuses(AllTestStatusesRequest(**user_parser.parse_args()))


class NextQuestion(Resource):
    @validate
    def get(self) -> QuestionResponse:
        """Получение следующего вопроса из укаанного теста для указанного юзера."""
        try:
            return obj_or_abort_404(
                TestService.get_next_question,
                NextQuestionRequest(**test_parser.parse_args()),
                TestNotFound,
                "Теста с заданным id не существует.",
            )
        except NoNextQuestion:
            return abort(HTTPStatus.NO_CONTENT, "Нет следующего вопроса.")


class SubmitAnswer(Resource):
    @validate
    def post(self) -> SubmitAnswerResponse:
        """Передача ответа от имени указанного юзера на указанный вопрос в тесте."""
        return obj_or_abort_404(
            TestService.process_answer,
            SubmitAnswerRequest(**answer_parser.parse_args()),
            (TestNotFound, TestQuestionNotFound),
            "Указанного вопроса не существует.",
        )


class CheckAnswer(Resource):
    @validate
    def get(self) -> CheckAnswerResponse:
        """Получение ранее внесенного ответа на указанный вопрос."""
        return obj_or_abort_404(
            TestService.check_answer,
            CheckAnswerRequest(**answer_parser.parse_args()),
            (TestNotFound, TestQuestionNotFound, AnswerNotFound),
            "Ответа на указанный вопрос не существует.",
        )
