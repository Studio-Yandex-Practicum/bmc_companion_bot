import json
from typing import List
from unittest import TestCase, mock

import pytest
from httpx import HTTPStatusError, RequestError
from pydantic import BaseModel
from src.core.constants import APIVersion, Endpoint, HTTPMethod
from src.request.clients import (
    APIClientRequestError,
    APIClientResponseError,
    APIClientValidationError,
    ObjAPIClient,
)


class ModelOne(BaseModel):
    text: str
    number: int


class ManyModelOne(BaseModel):
    __root__: List[ModelOne]


class ModelTwo(BaseModel):
    value: int


class ManyModelTwo(BaseModel):
    count: int
    values: List[ModelTwo]


test_object_1_data = {"text": "lorem ipsum", "number": 42}
test_object_1 = ModelOne(**test_object_1_data)
test_object_2_data = {"text": "dolor sit amet", "number": 69}
test_object_2 = ModelOne(**test_object_2_data)

test_objects_data = {"test_obj_1_id": test_object_1_data, "test_obj_2_id": test_object_2_data}
test_objects = [test_object_1, test_object_2]


test_client = ObjAPIClient(APIVersion.V1, Endpoint.MEETINGS, ModelOne, ManyModelOne)
test_client_of_wrong_model = ObjAPIClient(APIVersion.V1, Endpoint.MEETINGS, ModelTwo, ManyModelTwo)


def mocked_httpx_request(*args, **kwargs):
    """Имитация ответа httpx.request для тестирования src.request.clients.ObjAPIClient."""

    class FakeRequest:
        """Фиктивный запрос с полем url."""

        def __init__(self, url):
            self.url = url

    class MockResponse:
        """Фиктивный HTTP-ответ c полями status_code и json_data, поддерживающий методы json() и
        raise_for_status()."""

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code // 100 in [4, 5]:
                raise HTTPStatusError(
                    "error", response=self, request=FakeRequest(url=kwargs["url"])
                )

    if kwargs["url"].split("/")[-1] != Endpoint.MEETINGS.split("/")[-1]:
        obj_id = kwargs["url"].split("/")[-1]
    else:
        obj_id = None

    if obj_id == "initiate_RequestError":
        raise RequestError("error", request=FakeRequest(url=kwargs["url"]))

    if kwargs["method"] in [HTTPMethod.POST, HTTPMethod.PATCH]:
        return MockResponse(json.loads(kwargs["json"]), 200)
    if kwargs["method"] == HTTPMethod.DELETE:
        return MockResponse(test_objects_data[obj_id], 204)
    if kwargs["method"] == HTTPMethod.GET:
        if obj_id is not None:
            if obj_id not in test_objects_data:
                return MockResponse({"error": "not found"}, 404)
            return MockResponse(test_objects_data[obj_id], 200)
        return MockResponse([obj_data for obj_data in test_objects_data.values()], 200)
    return MockResponse(None, 400)


@mock.patch("src.request.clients.httpx.request", side_effect=mocked_httpx_request)
class TestObjAPIClient(TestCase):
    def test_create(self, mock_request):
        obj = test_client.create(test_object_1)
        assert obj == test_object_1

    def test_get(self, mock_request):
        obj = test_client.get("test_obj_1_id")
        assert isinstance(obj, ModelOne)
        assert obj == test_object_1
        objs = test_client.get()
        assert isinstance(objs, ManyModelOne)
        for test_object in test_objects:
            assert test_object in objs.__root__

    def test_update(self, mock_request):
        obj = test_client.update("test_obj_1_id", test_object_1)
        assert obj == test_object_1

    def test_delete(self, mock_request):
        obj = test_client.delete("test_obj_1_id")
        assert obj == test_object_1

    def test_request_error_catch(self, mock_request):
        with pytest.raises(APIClientRequestError):
            test_client.get("initiate_RequestError")

    def test_404_catch(self, mock_request):
        with pytest.raises(APIClientResponseError):
            test_client.get("nonexistent-id")

    def test_validation_error_catch(self, mock_request):
        with pytest.raises(APIClientValidationError):
            test_client_of_wrong_model.get()
