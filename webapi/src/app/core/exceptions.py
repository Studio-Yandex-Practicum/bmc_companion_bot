from http import HTTPStatus


class RoleNotExists(Exception):
    pass


class PhoneAlreadyExists(Exception):
    pass


class UserAlreadyBanned(Exception):
    pass


class TestAlreadyDeleted(Exception):
    pass


class UserNotExists(Exception):
    pass


errors = {
    "RoleNotExists": {"message": "Такой роли нет!", "status": HTTPStatus.NOT_FOUND},
    "PhoneAlreadyExists": {
        "message": "Пользователь с таким номером телефона уже есть!",
        "status": HTTPStatus.CONFLICT,
    },
    "UserAlreadyBanned": {"message": "Пользоваетель уже забанен!", "status": HTTPStatus.CONFLICT},
    "TestAlreadyDeleted": {"message": "Данный тест был удален!", "status": HTTPStatus.CONFLICT},
    "UserNotExists": {
        "message": "Пользователя с заданным id не существует.",
        "status": HTTPStatus.NOT_FOUND,
    },
}
