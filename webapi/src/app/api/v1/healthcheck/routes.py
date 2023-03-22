from datetime import datetime
from http import HTTPStatus

from app import db
from app.api.v1.healthcheck import bp
from app.models import User, UserTimeSlot
from flask import jsonify, request


@bp.route("/ping/")
def ping():
    return "pong", HTTPStatus.OK


def get_users(role_id=2):
    items = (
        db.session.query(User)
        .filter(User.role_id == role_id, User.deleted_at == None)  # noqa
        .all()
    )
    result = []
    for item in items:
        result.append(item.to_dict())
    return jsonify(result), HTTPStatus.OK


def get_timeslots(tg_login):
    user = db.session.query(User).filter(User.telegram_login == tg_login).first()
    items = (
        db.session.query(UserTimeSlot)
        .filter(UserTimeSlot.user_id == user.id, UserTimeSlot.deleted_at == None)  # noqa
        .all()
    )
    result = []
    for item in items:
        result.append(item.to_dict())
    return jsonify(result), HTTPStatus.OK


def get_user_by_tg_login(tg_login):
    item = db.session.query(User).filter(User.telegram_login == tg_login).first()
    result = item.to_dict() if item else {}
    return jsonify(result), HTTPStatus.OK


def create_user(user_params):
    item = User()
    for k, v in user_params.items():
        setattr(item, k, v)

    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), HTTPStatus.OK


def delete_user_by_id(user_id):
    item = db.session.query(User).filter(User.id == user_id).first()
    item.deleted_at = datetime.now()

    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), HTTPStatus.OK


def create_timeslot(tg_login, timeslot):
    item = db.session.query(User).filter(User.telegram_login == tg_login).first()
    if item:
        date_time_parts = timeslot.split(" ")
        date_time_str = (
            f"{date_time_parts[0]}/{date_time_parts[1]}/{date_time_parts[2]} "
            f"{date_time_parts[3]}:{date_time_parts[4]}:00"
        )
        date_time_obj = datetime.strptime(date_time_str, "%d/%m/%y %H:%M:%S")

        new_timeslot = UserTimeSlot()
        new_timeslot.user_id = item.id
        new_timeslot.date_start = date_time_obj

        db.session.add(new_timeslot)
        db.session.commit()

    return jsonify(item.to_dict()), HTTPStatus.OK


@bp.route("/", methods=["GET", "POST"])
def demo():
    data = request.get_json()
    callback = data.get("cb")
    if callback == "get_admins":
        return get_users(2)
    if callback == "get_users":
        return get_users(3)
    elif callback == "get_user_by_tg_login":
        tg_login = data.get("tg_login")
        return get_user_by_tg_login(tg_login)
    elif callback == "create_user":
        user_params = data.get("user_params")
        return create_user(user_params)
    elif callback == "create_user":
        user_params = data.get("user_params")
        return create_user(user_params)
    elif callback == "delete_user_by_id":
        user_id = data.get("user_id")
        return delete_user_by_id(user_id)
    elif callback == "get_timeslots":
        tg_login = data.get("tg_login")
        return get_timeslots(tg_login)
    elif callback == "create_timeslot":
        tg_login = data.get("tg_login")
        timeslot = data.get("timeslot")
        return create_timeslot(tg_login, timeslot)
