class CalendarException(Exception):
    """Общий класс исключений HTTP-обвязки Calendar."""

    pass


class CalendarRequestError(CalendarException):
    """Исключение неуспешного соединения с календарем."""

    pass
