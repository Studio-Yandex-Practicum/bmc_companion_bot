from pydantic import ValidationError


class APIException(Exception):
    pass


class APIClient:
    def __init__(self, endpoint_url, schema) -> None:
        self.schema = schema
        self.endpoint_url = endpoint_url

    def __validate__(self, json):
        try:
            self.schema.parse_obj(json)
        except ValidationError as e:
            raise APIException(e.json())
        return json

    def get(self, id=None, offset=None, limit=None):
        pass

    def create(self, obj):
        pass

    def update(self, id, obj):
        pass

    def delete(self, id):
        pass
