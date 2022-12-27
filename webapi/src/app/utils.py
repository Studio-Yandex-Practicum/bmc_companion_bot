from http import HTTPStatus

from flask import abort, jsonify, make_response


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
