from app.api.v1.users.routes import ApiUserWithID, ApiUserWithoutID
from app.api.v1.questions.routers import QuestionTypeApi, QuestionTypeAPIList
from app.api.v1.tests.routers import TestAPI, TestAPIList


def register_routes(api):
    api.add_resource(ApiUserWithoutID, "/api/v1/users")
    api.add_resource(ApiUserWithID, "/api/v1/users/<int:id>")

def register_router(api):
    api.add_resource(QuestionTypeApi, "/api/v1/questions/<int:id>")
    api.add_resource(QuestionTypeAPIList, "/api/v1/questions/")
    api.add_resource(TestAPIList, '/api/v1/tests/')
    api.add_resource(TestAPI, '/api/v1/tests/<int:test_id>/')
    