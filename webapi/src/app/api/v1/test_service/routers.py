from http import HTTPStatus

from app.schemas.requests import AllTestResultsRequest, TestResultRequest
from app.schemas.tests_completed import TestCompletedBare, TestCompletedList
from app.services.exceptions import TestCompletedNotFound
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
    def get(self) -> TestCompletedList:
        """Получение результатов всех тестов юзера с данным id."""
        test_results = TestService.get_all_test_results(
            AllTestResultsRequest(**user_parser.parse_args())
        )
        return test_results


class TestResult(Resource):
    @validate()
    def get(self) -> TestCompletedBare:
        """Получение результата конкретного теста юзера с данным id."""
        try:
            test_result = TestService.get_test_result(TestResultRequest(**test_parser.parse_args()))
        except TestCompletedNotFound:
            return abort(HTTPStatus.NOT_FOUND, "Результата теста с заданным id не существует.")
        return test_result
