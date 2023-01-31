from dataclasses import dataclass

import requests
from request.interfaces import IApiClient


@dataclass
class ApiClient(IApiClient):
    base_url: str = ""

    def get(self, url: str, params: dict | None = None, headers: dict | None = None):
        return requests.get(self.build_url(url), params=params, headers=headers)

    def post(self, url: str, data: dict | None = None, headers: dict | None = None):
        return requests.post(self.build_url(url), json=data, headers=headers)

    def patch(self, url: str, data: dict | None = None, headers: dict | None = None):
        return requests.patch(self.build_url(url), json=data, headers=headers)

    def delete(self, url: str, data: dict | None = None, headers: dict | None = None):
        return requests.delete(self.build_url(url), json=data, headers=headers)
