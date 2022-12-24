class APIClientException(Exception):
    """Общий класс исключений HTTP-обвязки APIClient."""

    pass


class APIClientRequestError(APIClientException):
    """Исключение ошибок соединения с Web-API."""

    pass


class APIClientResponseError(APIClientException):
    """Исключение неуспешных запросов к Web_API (статусы ответа 4xx и 5xx)."""

    pass


class APIClientValidationError(APIClientException):
    """Исключение ошибок валидации pydantic-моделей."""

    pass
