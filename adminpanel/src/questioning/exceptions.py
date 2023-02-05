class NoNextQuestion(Exception):
    """Нет следующего вопроса (тест пройден до конца)."""

    pass


class QuestionNotActive(Exception):
    """Не найден вопрос без ответа для данных user_id, test_id, question_id."""

    pass


class AnswerNotFound(Exception):
    """Не найден вариант ответа с данными question_id, answer_id."""

    pass


class ResultNotFound(Exception):
    """Не найден результат теста с данными user_id, test_id."""

    pass
