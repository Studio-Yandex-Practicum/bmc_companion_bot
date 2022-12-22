from typing import List

import pytest
from pydantic import BaseModel
from src.core.constants import Endpoint
from src.request.clients import APIClient, APIClientException


class ModelOne(BaseModel):
    text: str
    number: int


class ManyModelOne(BaseModel):
    __root__: List[ModelOne]


class ModelTwo(BaseModel):
    numbers: List[int]


test_client_one = APIClient(Endpoint.MEETINGS, ModelOne, ManyModelOne)


def test_exception():
    assert 0 == 0
    with pytest.raises(APIClientException):
        test_client_one.get()
