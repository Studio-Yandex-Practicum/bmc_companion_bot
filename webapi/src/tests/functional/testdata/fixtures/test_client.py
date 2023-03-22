import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def test_client(app):
    class TestClient:
        def __init__(self):
            self.client = app.test_client()
            self.base_url = "/api/v1"

        def get(self, url: str, params: dict | None = None, headers: dict | None = None):
            return self.client.get(self.base_url + url, query_string=params, headers=headers)

        def post(self, url: str, json: dict | None = None, headers: dict | None = None):
            return self.client.post(self.base_url + url, json=json, headers=headers)

    return TestClient()
