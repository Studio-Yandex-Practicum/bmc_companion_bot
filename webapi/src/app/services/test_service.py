from app.db.pg import db
from app.models import Answer, Test, TestCompleted, TestProgress, TestQuestion
from app.schemas.requests import (
    AllTestResultsRequest,
    AllTestStatusesRequest,
    CheckAnswerRequest,
    NextQuestionRequest,
    SubmitAnswerRequest,
    TestResultRequest,
    TestStatusRequest,
)
from app.schemas.responses import (
    AllTestResultsResponse,
    AllTestStatusesResponse,
    AnswerResponse,
    CheckAnswerResponse,
    QuestionResponse,
    SubmitAnswerResponse,
    TestInfoList,
    TestResultList,
    TestResultResponse,
    TestStatusResponse,
)
from app.services.exceptions import (
    AnswerNotFound,
    NoNextQuestion,
    TestNotFound,
    TestQuestionNotFound,
)
from core.constants import TestStatus


class TestService:
    def __validate_ids(self, test_question_id: int, answer_id: int) -> bool:
        if Answer.query(answer_id=answer_id, test_question_id=test_question_id).first() is None:
            raise AnswerNotFound
        return True

    def __complete_test(self, user_id: int, test_id: int) -> int:
        """Метод вычисления результата пройденного теста."""
        answer_ids = db.session.query(TestProgress.test_id).filter_by(
            user_id=user_id, test_id=test_id
        )
        answer_values = db.session.query(Answer.value).filter(Test.id.in_(answer_ids)).all()
        return sum(answer_values)

    def get_test_result(self, request: TestResultRequest) -> TestCompleted:
        user_id = request.user_id
        test_id = request.test_id
        test_result = TestCompleted.query.filter_by(user_id=user_id, test_id=test_id).first()
        if test_result is None:
            raise TestNotFound
        test_result_response = TestResultResponse.from_orm(test_result)
        return test_result_response

    def get_all_test_results(self, request: AllTestResultsRequest) -> AllTestResultsResponse:
        user_id = request.user_id
        test_results = TestCompleted.query.filter_by(user_id=user_id).all()
        data = {}
        data["user_id"] = user_id
        data["results"] = TestResultList.from_orm(test_results)
        return AllTestResultsResponse(**data)

    def get_all_test_statuses(self, request: AllTestStatusesRequest) -> AllTestStatusesResponse:
        user_id = request.user_id
        data = {}
        data["user_id"] = user_id
        active_test_ids = db.session.query(TestProgress.test_id).filter_by(
            user_id=user_id, answer_id=None
        )
        active_tests = db.session.query(Test).filter(Test.id.in_(active_test_ids)).all()
        data["active"] = TestInfoList.from_orm(active_tests)
        completed_test_ids = db.session.query(TestCompleted.test_id).filter_by(user_id=user_id)
        completed_tests = db.session.query(Test).filter(Test.id.in_(completed_test_ids)).all()
        data["completed"] = TestInfoList.from_orm(completed_tests)
        available_tests = (
            db.session.query(Test)
            .filter(~Test.id.in_(completed_test_ids))
            .filter(~Test.id.in_(active_test_ids))
            .all()
        )
        data["available"] = TestInfoList.from_orm(available_tests)
        return AllTestStatusesResponse(**data)

    def get_test_status(self, request: TestStatusRequest) -> TestStatusResponse:
        user_id = request.user_id
        test_id = request.test_id
        test = Test.query.get(test_id)
        if TestCompleted.query.filter_by(user_id=user_id, test_id=test_id).first() is not None:
            status = TestStatus.COMPLETED
        elif TestProgress.query.filter_by(user_id=user_id, test_id=test_id).first() is None:
            status = TestStatus.AVAILABLE
        else:
            status = TestStatus.ACTIVE
        return TestStatusResponse(user_id=user_id, test_id=test.id, name=test.name, status=status)

    def check_answer(self, request: CheckAnswerRequest) -> CheckAnswerResponse:
        user_id = request.user_id
        test_id = request.test_id
        test_question_id = request.test_question_id
        answer = Answer.query.filter_by(
            user_id=user_id, test_id=test_id, test_question_id=test_question_id
        ).first()
        if answer is None:
            raise AnswerNotFound
        answer_response = AnswerResponse.from_orm(answer)
        return answer_response

    def submit_answer(self, request: SubmitAnswerRequest) -> SubmitAnswerResponse:
        user_id = request.user_id
        test_id = request.test_id
        test_question_id = request.test_question_id
        answer_id = request.answer_id
        self.__validate_ids(test_question_id, answer_id)
        test_progress = TestProgress.query.filter_by(
            user_id=user_id, test_id=test_id, test_question_id=test_question_id, answer_id=None
        ).first()
        if test_progress is None:
            raise TestQuestionNotFound
        test_progress.answer_id = answer_id
        current_question = TestQuestion.query.get(test_progress.test_question_id)
        next_question_order_num = current_question.order_num + 1
        next_question = TestQuestion.query.filter(
            test_id=test_id, order_num=next_question_order_num
        ).first()
        if next_question is not None:
            new_progress = TestProgress(
                user_id=user_id, test_id=test_id, test_question_id=next_question.id
            )
            db.session.add(new_progress)
        else:
            value = self.__complete_test(user_id, test_id)
            test_completed = TestCompleted(user_id=user_id, test_id=test_id, value=value)
            db.session.add(test_completed)
        db.session.commit()
        return SubmitAnswerResponse.from_orm(test_progress)

    def get_next_question(self, request: NextQuestionRequest) -> QuestionResponse:
        user_id = request.user_id
        test_id = request.test_id
        if TestProgress.query.filter_by(user_id=user_id, test_id=test_id).first() is None:
            first_question = (
                TestQuestion.query(test_id=test_id).order_by(TestQuestion.order_num).first()
            )
            test_progress = TestProgress(
                user_id=user_id, test_id=test_id, test_question_id=first_question.id
            )
            db.session.add(test_progress)
            db.session.commit()
            return QuestionResponse.from_orm(first_question)
        test_progress = TestProgress.query.filter_by(
            user_id=user_id, test_id=test_id, answer_id=None
        ).first()
        if test_progress is None:
            raise NoNextQuestion
        next_question = TestQuestion.query.get(test_progress.test_question_id)
        return QuestionResponse.from_orm(next_question)
