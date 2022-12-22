from typing import Dict, List, Optional, Type, TypeVar, Union

import httpx
from core.constants import Endpoint, HTTPMethod
from core.settings import settings
from pydantic import BaseModel, ValidationError

WEB_API_URL = f"{settings.APP_HOST}:{settings.APP_PORT}"

ModelType = TypeVar("ModelType", bound=BaseModel)


class APIClientException(Exception):
    pass


class APIClient:
    def __init__(
        self, endpoint: Endpoint, model: Type[ModelType], manymodel: Type[ModelType]
    ) -> None:
        self.model = model
        self.manymodel = manymodel
        self.base_url = f"http://{WEB_API_URL}/{endpoint}"

    def _assert_response_ok(self, response: httpx.Response) -> httpx.Response:
        """
        Проверяет, что статус-код соответствует значению OK, и бросает исключение,
        если это не так.
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIClientException(
                f"Error response {e.response.status_code} after requesting {e.request.url}"
            )
        return response

    def _process_response(
        self, response: httpx.Response, pydantic_model: Type[ModelType]
    ) -> ModelType:
        """
        Принимает HTTP-запрос, проверяет, что статус-код соответствует OK, и преобразует его
        в объект модели pydantic.
        """
        response = self._assert_response_ok(response)
        try:
            obj = pydantic_model.parse_obj(response.json())
        except ValidationError as e:
            raise APIClientException(f"Unexpected format of API response: {e.json()}")
        return obj

    def _safe_request(
        self,
        method: str,
        url: str,
        json: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Метод, реализующий HTTP-запрос и перехват возникающих при этом исключений."""
        try:
            response = httpx.request(method=method, url=url, json=json, params=params)
        except httpx.RequestError as e:
            raise APIClientException(f"Error while requesting {e.request.url}")
        return response

    def _obj_url(self, id):
        """Конструирует URL ресурса, используя переданный id."""
        return f"{self.base_url}/{id}"

    def get(
        self,
        id: Optional[Union[int, str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Union[ModelType, List[ModelType]]:
        if id is not None:
            response = self._safe_request(HTTPMethod.GET, self._obj_url(id))
            obj = self._process_response(response, self.model)
            return obj
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        print(params)
        response = self._safe_request(HTTPMethod.GET, self.base_url, params=params)
        objs = self._process_response(response, self.manymodel)
        return objs

    def create(self, obj: ModelType) -> ModelType:
        response = self._safe_request(HTTPMethod.POST, self.base_url, json=obj.json())
        obj = self._process_response(response, self.model)
        return obj

    def update(self, id: Union[int, str], obj: ModelType) -> ModelType:
        response = self._safe_request(HTTPMethod.PATCH, self._obj_url(id), json=obj.json())
        obj = self._process_response(response, self.model)
        return obj

    def delete(self, id: Union[int, str]) -> ModelType:
        response = self._safe_request(HTTPMethod.DELETE, self._obj_url(id))
        obj = self._process_response(response, self.model)
        return obj
