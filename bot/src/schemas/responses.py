from pydantic import BaseModel


class TestInfo(BaseModel):
    """Модель информации о тесте."""

    id: int
    type: int
    name: str


class TestResult(TestInfo):
    """Модель информации о результате теста."""

    value: int


class TestInfoList(BaseModel):
    """Модель списка информации о тестах."""

    __root__: list[TestInfo]

    @property
    def items(self):
        return self.__root__


class TestResultList(BaseModel):
    """Модель списка результатов теста."""

    __root__: list[TestResult]

    @property
    def items(self):
        return self.__root__


class AllTestStatusesResponse(BaseModel):
    """Модель ответа с информацией о статусе всех тестов для данного юзера."""

    user_id: int
    available: TestInfoList
    active: TestInfoList
    completed: TestInfoList


class TestResultResponse(TestResult):
    """Модель ответа с результатом конкретного теста для данного юзера."""

    user_id: int


class AnswerInfo(BaseModel):
    """Модель информации об ответе на вопрос теста."""

    id: int
    text: str


class AnswerInfoList(BaseModel):
    """Модель cписка информации об ответе на вопрос теста."""

    __root__: list[AnswerInfo]

    @property
    def items(self):
        return self.__root__


class QuestionResponse(BaseModel):
    """Модель ответа на запрос следующего вопроса указанного теста для указанного юзера."""

    user_id: int
    test_id: int
    id: int
    text: str
    answers: AnswerInfoList


class SubmitAnswerResponse(BaseModel):
    """Модель ответа на POST-запрос внесения ответа на вопрос теста."""

    user_id: int
    test_id: int
    test_question_id: int
    answer_id: int


class UserResponse(BaseModel):
    """Модель для получения краткой информации о пользователе."""

    id: int | None
    username: str | None = ""
    first_name: str | None = ""
    last_name: str | None = ""
    middle_name: str | None = ""
    email: str | None = ""
    phone: str | None = ""
    age: int | None = 0
    uce_score: int | None = 0
    chat_id: str | None = ""
    telegram_login: str | None = ""
    telegram_id: str | None = ""
    address: str | None = ""


class TimeslotResponse(BaseModel):
    """Модель для получения краткой информации о таймслоте."""

    id: int | None
    date_start: str | None = ""
    profile: UserResponse | None = None


class MeetingResponse(BaseModel):
    """Модель для получения краткой информации о митинга (встречи)."""

    id: int | None
    psychologist: int | None = None
    user: int | None = None
    comment: str | None = ""
    format: int | None = None
    date_start: str | None = ""
    timeslot: int | None


class FeedbackResponse(BaseModel):
    """Модель для получения краткой информации о отзыве."""

    id: int | None
    meeting: int | None = None
    user: int | None = None
    text: str | None = None
    comfort_score: int | None = None
    better_score: int | None = None


class UceTestResponse(BaseModel):
    """Модель информации о id теста."""

    id: int
