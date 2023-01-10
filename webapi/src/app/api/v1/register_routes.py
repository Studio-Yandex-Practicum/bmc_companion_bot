from app.api.v1.questions.routers import (
    QuestionAPIList,
    QuestionTypeAPI,
    QuestionTypeAPIList,
    QuetionAPI,
)
from app.api.v1.tests.routers import (
    TestAPI,
    TestAPIList,
    TestCompletedAPI,
    TestCompletedAPIList,
    TestProgressAPI,
    TestProgressAPIList,
)
from app.api.v1.users.routes import ApiUserWithID, ApiUserWithoutID


def register_routes(api):
    api.add_resource(ApiUserWithoutID, "/api/v1/users")
    api.add_resource(ApiUserWithID, "/api/v1/users/<int:id>")
    api.add_resource(QuestionTypeAPI, "/api/v1/question-type/<int:id>")
    api.add_resource(QuestionTypeAPIList, "/api/v1/question-type/")
    api.add_resource(QuetionAPI, "/api/v1/questions/<int:id>")
    api.add_resource(QuestionAPIList, "/api/v1/questions/")
    api.add_resource(TestAPIList, "/api/v1/tests/")
    api.add_resource(TestAPI, "/api/v1/tests/<int:test_id>/")
    api.add_resource(TestProgressAPIList, "/api/v1/tests/progress/")
    api.add_resource(TestProgressAPI, "/api/v1/tests/progress/<int:progress_id>/")
    api.add_resource(TestCompletedAPIList, "/api/v1/tests/completed/")
    api.add_resource(TestCompletedAPI, "/api/v1/tests/completed/<int:completed_id>/")
