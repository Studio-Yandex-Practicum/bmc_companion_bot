class MenuElement:
    def __init__(self, name: str, result: str, answers: dict[str, str]) -> None:
        self.name = name
        self.result = result
        self.answers = answers

    def __call__(self, answer_name: str) -> str:
        return self.answers[answer_name]


class MenuNames:
    """Текстовое описание для элементов меню."""

    start_menu = MenuElement(
        name="Меню",
        result="""Привет, {}! Мы приветствуем Ваше решение разобраться в себе.
В нашем проекте есть настоящие профессионалы, которые помогут Вам сделать это.""",
        answers={"to_test": "Пройти тестирование", "to_meeting": "Записаться к психологу"},
    )
