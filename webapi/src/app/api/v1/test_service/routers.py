from http import HTTPStatus

from app.schemas.requests import (
    AllTestResultsRequest,
    AllTestStatusesRequest,
    AnswerRequest,
    NextQuestionRequest,
    TestResultRequest,
    TestStatusRequest,
)
from app.schemas.responses import (
    AllTestResultsResponse,
    AllTestStatusesResponse,
    AnswerResponse,
    CheckAnswerResponse,
    QuestionResponse,
    TestResultResponse,
    TestStatusResponse,
)
from app.services.exceptions import (
    AnswerNotFound,
    NoNextQuestion,
    TestNotFound,
    TestQuestionNotFound,
)
from app.services.test_service import TestService
from flask import abort
from flask_pydantic import validate
from flask_restful import Resource, reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument("user_id", type=int, required=True)
test_parser = user_parser.copy()
test_parser.add_argument("user_id", type=int, required=True)
question_parser = test_parser.copy()
question_parser.add_argument("question_id", type=int, required=True)
answer_parser = question_parser.copy()
answer_parser.add_argument("answer_id", type=int, required=True)


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
        try:
            test_result = TestService.get_test_result(TestResultRequest(**test_parser.parse_args()))
        except TestNotFound:
            return abort(HTTPStatus.NOT_FOUND, "Результата теста с заданным id не существует.")
        return test_result


class TestStatus(Resource):
    @validate()
    def get(self) -> TestStatusResponse:
        """Получение статуса конкретного теста для юзера с данным id."""
        try:
            test_status = TestService.get_test_status(TestStatusRequest(**test_parser.parse_args()))
        except TestNotFound:
            return abort(HTTPStatus.NOT_FOUND, "Теста с заданным id не существует.")
        return test_status


class AllTestStatuses(Resource):
    @validate()
    def get(self) -> AllTestStatusesResponse:
        """Получение статуса всех тестов для юзера с даннным id."""
        test_results = TestService.get_all_test_statuses(
            AllTestStatusesRequest(**user_parser.parse_args())
        )
        return test_results


class NextQuestion(Resource):
    @validate
    def get(self) -> QuestionResponse:
        """Получение следующего вопроса из укаанного теста для указанного юзера."""
        try:
            next_question = TestService.get_next_question(
                NextQuestionRequest(**test_parser.parse_args())
            )
        except TestNotFound:
            return abort(HTTPStatus.NOT_FOUND, "Теста с заданным id не существует.")
        except NoNextQuestion:
            return abort(HTTPStatus.NO_CONTENT, "Нет следующего вопроса.")
        return next_question


class SubmitAnswer(Resource):
    @validate
    def post(self) -> AnswerResponse:
        """Передача ответа от имени указанного юзера на указанный вопрос в тесте."""
        try:
            answer = TestService.process_answer(AnswerRequest(**answer_parser.parse_args()))
        except (TestNotFound, TestQuestionNotFound):
            return abort(HTTPStatus.NOT_FOUND, "Указанного вопроса не существует.")
        return answer


class CheckAnswer(Resource):
    @validate
    def get(self) -> CheckAnswerResponse:
        """Получение ранее внесенного ответа на указанный вопрос."""
        try:
            answer = TestService.check_answer(AnswerRequest(**answer_parser.parse_args()))
        except (TestNotFound, TestQuestionNotFound, AnswerNotFound):
            return abort(HTTPStatus.NOT_FOUND, "Ответа на указанный вопрос не существует.")
        return answer
