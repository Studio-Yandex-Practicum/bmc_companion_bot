import httpx
from core.settings import settings
from pydantic import ValidationError

WEB_API_URL = f"{settings.APP_HOST}:{settings.APP_PORT}"


class APIException(Exception):
    pass


class APIClient:
    def __init__(self, endpoint, model) -> None:
        self.model = model
        self.base_url = f"{WEB_API_URL}/{endpoint}"

    def __validate__(self, json):
        try:
            obj = self.model.parse_obj(json)
        except ValidationError as e:
            raise APIException(e.json())
        return obj

    def __obj_url__(self, id=None):
        if id:
            return self.base_url + f"/{id}"
        return self.base_url

    def get(self, id=None, offset=None, limit=None):
        if id is not None:
            url = self.__obj_url__(id=id)
            response = httpx.get(url)
            obj = self.__validate__(response.json())
            return obj
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        response = httpx.get(self.base_url, params=params)
        objs = []
        for json in response.json():
            objs.append(self.__validate__(json))
        return objs

    def create(self, obj):
        url = self.__obj_url__()
        response = httpx.post(url, data=obj.json())
        obj = self.__validate__(response.json())
        return obj

    def update(self, id, obj):
        url = self.__obj_url__(id=id)
        response = httpx.patch(url, data=obj.json())
        obj = self.__validate__(response.json())
        return obj

    def delete(self, id):
        url = self.__obj_url__(id=id)
        response = httpx.delete(url)
        obj = self.__validate__(response.json())
        return obj
