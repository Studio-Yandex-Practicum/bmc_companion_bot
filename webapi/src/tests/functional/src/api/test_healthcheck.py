from http import HTTPStatus


def test_healthcheck(test_client):
    response = test_client.get("/healthcheck/ping/")

    assert response.status_code == HTTPStatus.OK
