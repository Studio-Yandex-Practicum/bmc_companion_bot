from http import HTTPStatus

from flask import abort, jsonify, make_response


def abort_json(msg: str, status_code: int = HTTPStatus.BAD_REQUEST):
    abort(make_response(jsonify(msg=msg), status_code))
