from enum import Enum


class Endpoint(str, Enum):
    MEETINGS = "api/v1/meetings"
    TESTS = "api/v1/tests"
    USERS = "api/v1/users"


class HTTPMethod(str, Enum):
    CONNECT = "CONNECT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    GET = "GET"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


class UserRole(int, Enum):
    ROOT = 1
    ADMIN = 2
    USER = 3
