class APIClientException(Exception):
    """Общий класс исключений HTTP-обвязки APIClient."""

    pass


class NoNextQuestion(Exception):
    """Исключение отсутствия следующего вопроса (тест пройден до конца)."""

    pass
