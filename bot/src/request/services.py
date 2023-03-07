from dataclasses import dataclass
from http import HTTPStatus
from typing import Type

from core.constants import KEY_RESULTS_FOR_PAGINATED_RESPONSE
from pydantic import BaseModel
from request.base import ApiClient
from utils import is_paginated_object


@dataclass
class PydanticApiService:
    api_client: ApiClient

    def get(
        self,
        model: Type[BaseModel],
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
    ):
        return self._send_request("get", url, model, params=params, headers=headers)

    def post(
        self,
        model: Type[BaseModel],
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ):
        return self._send_request("post", url, model, data=data, headers=headers)

    def patch(
        self,
        model: Type[BaseModel],
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ):
        return self._send_request("patch", url, model, data=data, headers=headers)

    def delete(
        self,
        model: Type[BaseModel],
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ):
        return self._send_request("delete", url, model, data=data, headers=headers)

    def _send_request(self, method: str, url: str, model: Type[BaseModel], **kwargs):
        response = getattr(self.api_client, method)(url, **kwargs)

        if method == "delete" and response.status_code == HTTPStatus.NO_CONTENT:
            return None

        data = response.json()

        if is_paginated_object(data):
            data = data[KEY_RESULTS_FOR_PAGINATED_RESPONSE]

        if isinstance(data, dict):
            return model(**data)

        if isinstance(data, list):
            return [model(**item) for item in data]

        raise ValueError(f"Invalid data format: {data}")
