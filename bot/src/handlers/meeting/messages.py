LETS_CHECK = "Давайте все проверим:"
LENGTH = "Длительность встречи: 50 мин."
FORMAT = "Формат записи: "
FORMAT_ONLINE = "Онлайн"
FORMAT_OFFLINE = "Очно"
ADDRESS = "Адрес: "
DEFAULT_ADDRESS = "ул. Дуки, д.86"
PSYCHOLOGIST = "Психолог: "
DATE = "Дата и время: "
YOU_WERE = "Вы уже были у этих психологов:"
YOU_WERENT = "\nУ этих психологов Вы еще не были:"
NEW_MEETING = "У вас новая запись:\n"
PATIENT = "Пациент: "
PHONE = "Телефон: "
CHOOSE_DATE = "Введите порядковый номер консультации:\n"


async def psychologist_meeting_message(format, user, timeslot, header=NEW_MEETING):
    text = [header]
    text += [PATIENT + f"{user.first_name} {user.last_name}"]
    text += [PHONE + f"{user.phone}"]
    text += [DATE + f"{timeslot.date_start}"]
    text += [FORMAT + f"{format}"]
    if format == FORMAT_OFFLINE:
        text += [ADDRESS + f" {DEFAULT_ADDRESS}"]
    return "\n".join(text)


async def user_check_meeting_message(format, first_name, last_name, date, address=DEFAULT_ADDRESS):
    text = [
        LETS_CHECK,
        LENGTH,
    ]
    text += [
        FORMAT + f"{format}",
    ]
    if format == FORMAT_OFFLINE:
        text += [
            ADDRESS + f"{address}",
        ]
    text += [
        PSYCHOLOGIST + f"{first_name} {last_name}",
    ]
    text += [
        DATE + f"{date}",
    ]
    return "\n".join(text)


async def user_choose_timeslot_message(timeslots, psycho_set={}, is_sixth_meeting=False):
    text = [CHOOSE_DATE]
    if is_sixth_meeting:
        text.append(
            "Вы побывали на 5 бесплатных консультациях, стоимость консультации для вас - 800р"
            + "(обычная цена - 2000р)\n"
        )
    list_was = []
    list_was_not = []
    for index, timeslot in enumerate(timeslots, start=1):
        timeslot_data = (
            f"{index}. {timeslot.profile.first_name} "
            f"{timeslot.profile.last_name}: "
            f"{timeslot.date_start}"
        )
        if timeslot.date_start and timeslot.profile:
            ts_psycho = timeslot.profile.id
            if ts_psycho in psycho_set:
                list_was.append(timeslot_data)
            else:
                list_was_not.append(timeslot_data)
    if len(list_was + list_was_not) < 1:
        return None
    if not all((list_was, list_was_not)):
        return "\n".join(text + list_was + list_was_not)
    return "\n".join(text + [YOU_WERE] + list_was + [YOU_WERENT] + list_was_not)
