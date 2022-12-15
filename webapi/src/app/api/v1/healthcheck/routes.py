from http import HTTPStatus

from app.api.v1.healthcheck import bp


@bp.route("/ping/")
def ping():
    return "pong", HTTPStatus.OK
