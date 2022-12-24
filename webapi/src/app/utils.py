from http import HTTPStatus

from flask import abort, jsonify, make_response


def abort_json(msg: str, status_code: int = HTTPStatus.BAD_REQUEST):
    abort(make_response(jsonify(msg=msg), status_code))


# def get_paginated_list(results, url, start, limit):
#     start = int(start)
#     limit = int(limit)
#     count = len(results)
#     if count < start or limit < 0:
#         abort(404)
#     objects = {}
#     objects["start"] = start
#     objects["limit"] = limit
#     objects["count"] = count
#     if start == 1:
#         objects["previous"] = ""
#     else:
#         start_copy = max(1, start - limit)
#         limit_copy = start - 1
#         objects["previous"] = url + "?start=%d&limit=%d" % (start_copy, limit_copy)
#     if start + limit > count:
#         objects["next"] = ""
#     else:
#         start_copy = start + limit
#         objects["next"] = url + "?start=%d&limit=%d" % (start_copy, limit)
#     objects["users"] = results[(start - 1) : (start - 1 + limit)]
#     return objects
