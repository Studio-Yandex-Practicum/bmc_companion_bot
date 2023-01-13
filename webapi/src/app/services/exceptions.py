class TestNotFound(Exception):
    """Не существует теста(-ов) с указанными параметрами."""

    pass


class TestQuestionNotFound(Exception):
    """Не существует вопроса с указанными параметрами."""

    pass


class NoNextQuestion(Exception):
    """Нет следующего вопроса (тест пройден до конца)."""

    pass


class AnswerNotFound(Exception):
    """Не существует ответа на вопрос теста с указанными параметрами."""

    pass
