from app.api.v1.questions.routers import QuestionTypeApi, QuestionTypeAPIList
from app.api.v1.users.routes import ApiUserWithID, ApiUserWithoutID


def register_routes(api):
    api.add_resource(ApiUserWithoutID, "/api/v1/users")
    api.add_resource(ApiUserWithID, "/api/v1/users/<int:id>")
    api.add_resource(QuestionTypeApi, "/api/v1/questions/<int:id>")
    api.add_resource(QuestionTypeAPIList, "/api/v1/questions/")
