import httpx
from core.settings import settings
from pydantic import ValidationError

WEB_API_URL = f"{settings.APP_HOST}:{settings.APP_PORT}"


class APIClientException(Exception):
    pass


class APIClient:
    def __init__(self, endpoint, model, manymodel):
        self.model = model
        self.manymodel = manymodel
        self.base_url = f"http://{WEB_API_URL}/{endpoint}"

    def __assert_response_ok(self, response):
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIClientException(
                f"Error response {e.response.status_code} after requesting {e.request.url}"
            )
        return response

    def __process_response(self, response, pydantic_model):
        response = self.__assert_response_ok(response)
        try:
            obj = pydantic_model.parse_obj(response.json())
        except ValidationError as e:
            raise APIClientException(f"Unexpected format of API response: {e.json()}")
        return obj

    def __safe_request(self, method, url, json=None, params=None):
        try:
            response = httpx.request(method=method, url=url, json=json, params=params)
        except httpx.RequestError as e:
            raise APIClientException(f"Error while requesting {e.request.url}")
        return response

    def __obj_url(self, id):
        return f"{self.base_url}/{id}"

    def get(self, id=None, offset=None, limit=None):
        if id is not None:
            response = self.__safe_request("GET", self.__obj_url(id))
            obj = self.__process_response(response, self.model)
            return obj
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        print(params)
        response = self.__safe_request("GET", self.base_url, params=params)
        objs = self.__process_response(response, self.manymodel)
        return objs

    def create(self, obj):
        response = self.__safe_request("POST", self.base_url, json=obj.json())
        obj = self.__process_response(response, self.model)
        return obj

    def update(self, id, obj):
        response = self.__safe_request("PATCH", self.__obj_url(id), json=obj.json())
        obj = self.__process_response(response, self.model)
        return obj

    def delete(self, id):
        response = self.__safe_request("DELETE", self.__obj_url(id))
        obj = self.__process_response(response, self.model)
        return obj
