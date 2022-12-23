from typing import Dict, Optional, Type, TypeVar, Union

import httpx
from core.constants import Endpoint, HTTPMethod
from core.settings import settings
from pydantic import BaseModel, ValidationError
from request.exceptions import (
    APIClientRequestError,
    APIClientResponseError,
    APIClientValidationError,
)

WEB_API_URL = f"{settings.APP_HOST}:{settings.APP_PORT}"

ModelType = TypeVar("ModelType", bound=BaseModel)


class APIClient:
    """
    Класс обвязки HTTP-запросов к Web-API. Конструктор принимает адрес эндпойнта, тип
    pydantic-модели отдельного объекта и тип pydantic-модели их набора. Поддерживаются методы
    get(), create(), patch() и delete().
    """

    def __init__(
        self, endpoint: Endpoint, model: Type[ModelType], many_model: Type[ModelType]
    ) -> None:
        self.model = model
        self.many_model = many_model
        self.base_url = f"http://{WEB_API_URL}/{endpoint}"

    def _assert_response_ok(self, response: httpx.Response) -> httpx.Response:
        """Выбрасывает APIClientResponseError, если код состояния HTTP-ответа не OK."""
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIClientResponseError(
                f"Error response {e.response.status_code} after requesting {e.request.url}"
            )
        return response

    def _process_response(
        self, response: httpx.Response, pydantic_model: Type[ModelType]
    ) -> ModelType:
        """
        Принимает HTTP-ответ, проверяет, что код состояния -- OK, и преобразует его
        в объект модели pydantic. Выбрасывает APIClientValidationError, если полученный JSON
        не соответствует модели.
        """
        response = self._assert_response_ok(response)
        try:
            obj = pydantic_model.parse_obj(response.json())
        except ValidationError as e:
            raise APIClientValidationError(f"Unexpected format of API response: {e.json()}")
        return obj

    def _safe_request(
        self,
        method: str,
        url: str,
        json: Optional[str] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """Выполняет HTTP-запрос и перехватывает исключения, выбрасывая APIClientRequestError."""
        try:
            response = httpx.request(method=method, url=url, json=json, params=params)
        except httpx.RequestError as e:
            raise APIClientRequestError(f"Error while requesting {e.request.url}")
        return response

    def _obj_url(self, id: Union[int, str]) -> str:
        """Конструирует URL конкретного ресурса, используя переданный id."""
        return f"{self.base_url}/{id}"

    def get(
        self,
        id: Optional[Union[int, str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> ModelType:
        """
        Получение объекта(-ов). Принимает id объекта или необязательные значения offset и/или
        limit, возвращает pydantic-модель одиночного объекта или их набора.
        """
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
        objs = self._process_response(response, self.many_model)
        return objs

    def create(self, obj: ModelType) -> ModelType:
        """
        Создание объекта. Принимает pydantic-модель одиночного объекта, возвращает pydantic-модель
        одиночного объекта, сконструированную по json-данным ответа Web-API.
        """
        response = self._safe_request(HTTPMethod.POST, self.base_url, json=obj.json())
        obj = self._process_response(response, self.model)
        return obj

    def update(self, id: Union[int, str], obj: ModelType) -> ModelType:
        """
        Редактирование объекта. Принимает id объекта в базе и pydantic-модель одиночного объекта,
        возвращает pydantic-модель, сконструированную по json-данным ответа Web-API.
        """
        response = self._safe_request(HTTPMethod.PATCH, self._obj_url(id), json=obj.json())
        obj = self._process_response(response, self.model)
        return obj

    def delete(self, id: Union[int, str]) -> ModelType:
        """
        Удаление объектов. Принимает id объекта в базе, возвращает pydantic-модель,
        сконструированную по json-данным ответа Web-API.
        """
        response = self._safe_request(HTTPMethod.DELETE, self._obj_url(id))
        obj = self._process_response(response, self.model)
        return obj
