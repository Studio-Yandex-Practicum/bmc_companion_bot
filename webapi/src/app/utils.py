from http import HTTPStatus
from typing import Callable, TypeVar, Union

from flask import abort, jsonify, make_response
from pydantic import BaseModel

RequestType = TypeVar("RequestType", bound=BaseModel)
ResponseType = TypeVar("ResponseType", bound=BaseModel)
ExceptionType = TypeVar("ExceptionType", bound=Exception)


def obj_or_abort_404(
    service_method: Callable[[RequestType], ResponseType],
    request: RequestType,
    not_found_exceptions: Union[ExceptionType, tuple[ExceptionType]],
    not_found_message: str,
) -> ResponseType:
    try:
        return service_method(request)
    except not_found_exceptions:
        return abort(HTTPStatus.NOT_FOUND, not_found_message)


def abort_json(msg: str, status_code: int = HTTPStatus.BAD_REQUEST):
    abort(make_response(jsonify(msg=msg), status_code))


def get_paginated_list(data, url, query):
    start = query.start
    limit = query.limit
    count = len(data)
    if count < start or limit < 0:
        abort(404)
    objects = {}
    objects["start"] = start
    objects["limit"] = limit
    objects["count"] = count
    if start == 1:
        objects["previous"] = ""
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        objects["previous"] = url + "?start=%d&limit=%d" % (start_copy, limit_copy)
    if start + limit > count:
        objects["next"] = ""
    else:
        start_copy = start + limit
        objects["next"] = url + "?start=%d&limit=%d" % (start_copy, limit)
    start_paginate = start - 1
    limit_paginate = start - 1 + limit
    objects["data"] = data[start_paginate:limit_paginate]
    return objects
