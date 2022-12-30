from app.api.v1.meetings.routers import MeetingTypeAPI, MeetingTypeAPIList
from app.api.v1.questions.routers import QuestionTypeApi, QuestionTypeAPIList
from app.api.v1.users.routes import ApiUserWithID, ApiUserWithoutID


def register_routes(api):
    api.add_resource(ApiUserWithoutID, "/api/v1/users")
    api.add_resource(ApiUserWithID, "/api/v1/users/<int:id>")
    api.add_resource(QuestionTypeApi, "/api/v1/questions/<int:id>")
    api.add_resource(QuestionTypeAPIList, "/api/v1/questions/")
    api.add_resource(MeetingTypeAPI, "/api/v1/meeting_types/<int:meeting_type_id>")
    api.add_resource(MeetingTypeAPIList, "/api/v1/meeting_types/")
