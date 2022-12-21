from ui import constants as const


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
        name=const.NAME,
        result=const.GREETING_MESSAGE,
        answers=const.ANSWERS,
    )
