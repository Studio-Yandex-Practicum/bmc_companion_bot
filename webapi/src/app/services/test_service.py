from app.models import TestCompleted
from app.schemas.requests import AllTestResultsRequest, TestResultRequest
from app.schemas.tests_completed import TestCompletedBare, TestCompletedList
from app.services.exceptions import TestCompletedNotFound


class TestService:
    def get_all_test_results(self, request: AllTestResultsRequest) -> TestCompletedList:
        user_id = request.user_id
        test_results = TestCompleted.query.filter_by(user_id=user_id).all()
        test_results = TestCompletedList.from_orm(test_results)
        return test_results

    def get_test_result(self, request: TestResultRequest) -> TestCompleted:
        user_id = request.user_id
        test_id = request.test_id
        test_result = TestCompleted.query.filter_by(user_id=user_id, test_id=test_id).first()
        if test_result is None:
            raise TestCompletedNotFound
        test_result = TestCompletedBare.from_orm(test_result)
        return test_result
