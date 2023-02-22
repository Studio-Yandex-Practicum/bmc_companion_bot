from abc import ABC, abstractmethod
from urllib.parse import urljoin


class IApiClient(ABC):
    @property
    @abstractmethod
    def base_url(self):
        pass

    @base_url.setter
    @abstractmethod
    def base_url(self, val):
        pass

    @abstractmethod
    def get(self, url: str, params: dict | None = None, headers: dict | None = None):
        pass

    @abstractmethod
    def post(self, url: str, data: dict | None = None, headers: dict | None = None):
        pass

    @abstractmethod
    def patch(self, url: str, data: dict | None = None, headers: dict | None = None):
        pass

    @abstractmethod
    def delete(self, url: str, data: dict | None = None, headers: dict | None = None):
        pass

    def build_url(self, url: str) -> str:
        return urljoin(self.base_url, url)
