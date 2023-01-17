from app.api.v1.meetings.routers import MeetingTypeAPI, MeetingTypeAPIList
from app.api.v1.questions.routers import (
    QuestionAPIList,
    QuestionTypeAPI,
    QuestionTypeAPIList,
    QuetionAPI,
)
from app.api.v1.test_service.routers import (
    AllTestResults,
    AllTestStatuses,
    CheckAnswer,
    NextQuestion,
    SubmitAnswer,
    TestResult,
    TestStatus,
)
from app.api.v1.tests.routers import (
    TestAPI,
    TestAPIList,
    TestCompletedAPI,
    TestCompletedAPIList,
    TestProgressAPI,
    TestProgressAPIList,
)
from app.api.v1.user_time_slot.routers import UserTimeSlotAPI, UserTimeSlotAPIList
from app.api.v1.users.routes import ApiUserWithID, ApiUserWithoutID


def register_routes(api):
    api.add_resource(ApiUserWithoutID, "/api/v1/users/")
    api.add_resource(ApiUserWithID, "/api/v1/users/<int:id>")
    api.add_resource(QuestionTypeAPI, "/api/v1/question-type/<int:id>")
    api.add_resource(QuestionTypeAPIList, "/api/v1/question-type/")
    api.add_resource(QuetionAPI, "/api/v1/questions/<int:id>")
    api.add_resource(QuestionAPIList, "/api/v1/questions/")
    api.add_resource(MeetingTypeAPI, "/api/v1/meeting_types/<int:meeting_type_id>")
    api.add_resource(MeetingTypeAPIList, "/api/v1/meeting_types/")
    api.add_resource(TestAPIList, "/api/v1/tests/")
    api.add_resource(TestAPI, "/api/v1/tests/<int:test_id>/")
    api.add_resource(TestProgressAPIList, "/api/v1/tests/progress/")
    api.add_resource(TestProgressAPI, "/api/v1/tests/progress/<int:progress_id>/")
    api.add_resource(TestCompletedAPIList, "/api/v1/tests/completed/")
    api.add_resource(TestCompletedAPI, "/api/v1/tests/completed/<int:completed_id>/")
    api.add_resource(AllTestResults, "/api/v1/test_results/all/")
    api.add_resource(TestResult, "/api/v1/test_results/")
    api.add_resource(AllTestStatuses, "/api/v1/test_statuses/all/")
    api.add_resource(TestStatus, "/api/v1/test_statuses/get/")
    api.add_resource(NextQuestion, "/api/v1/next_question/")
    api.add_resource(SubmitAnswer, "/api/v1/submit_answer/")
    api.add_resource(CheckAnswer, "/api/v1/check_answer/")
    api.add_resource(UserTimeSlotAPI, "/api/v1/slot/<int:id>")
    api.add_resource(UserTimeSlotAPIList, "/api/v1/slots/")
