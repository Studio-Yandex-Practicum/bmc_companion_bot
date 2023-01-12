from app.api.v1.users.routes import ApiUserWithID, ApiUserWithoutID


def register_routes(api):
    api.add_resource(ApiUserWithoutID, "/api/v1/users")
    api.add_resource(ApiUserWithID, "/api/v1/users/<int:id>")
