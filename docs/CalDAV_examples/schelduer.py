import os
from datetime import datetime, timedelta

import caldav
from dotenv import load_dotenv

load_dotenv()

caldav_url = os.getenv("CAL_URL")
username = os.getenv("CAL_USER")
password = os.getenv("CAL_PASS")

client = caldav.DAVClient(url=caldav_url, username=username, password=password)

# Процесс выбора и получения календаря.
my_principal = client.principal()
calendars = my_principal.calendars()
ya_calendar = calendars[0]


def scheldue_appointment(summary_old, summary_new):
    # Ищет ивенты в ближайшие 7 дней от момента запроса.
    events_fetched = ya_calendar.search(
        start=datetime.now(), end=(datetime.now() + timedelta(days=7)), event=True, expand=True
    )
    # Фильтрует ивенты по тексту в них.
    for event in events_fetched:
        if event.vobject_instance.vevent.summary.value == summary_old:
            # Редактирует текст в ивенте.
            event.vobject_instance.vevent.summary.value = summary_new
            event.save()
            return f"Вы успешно записались в {summary_old}"
        return "Кто-то уже записался в этот слот"


# Добавляет ивент с заданной датой и содержимым.
def add_event(date_start, summary):
    ya_calendar.save_event(
        dtstart=date_start,
        dtend=(date_start + timedelta(hours=1)),
        dtstamp=datetime.now(),
        summary=f"{summary}",
    )


if __name__ == "__main__":
    # Ищет ивент и печатает его саммари.
    events_fetched = ya_calendar.search(
        start=datetime(2022, 12, 27), end=datetime(2022, 12, 31), event=True, expand=True
    )
    print(events_fetched[0].vobject_instance.vevent.summary.value)

    # Вызывает функцию, меняющую саммари ивента.
    print(scheldue_appointment("Слот 2", "Иван Иванов с 12 до 13"))

    # Ищет ивент снова и печатает его саммари, проверяя, изменилось ли оно.
    events_fetched2 = ya_calendar.search(
        start=datetime(2022, 12, 27), end=datetime(2022, 12, 31), event=True, expand=True
    )
    print(events_fetched2[0].vobject_instance.vevent.summary.value)

    ev_date = datetime(2023, 1, 13, 14)
    ev_summ = "Иванов к доктору Петрову"
    # add_event(ev_date, ev_summ)
    events_fetched3 = ya_calendar.search(
        start=datetime(2023, 1, 12), end=datetime(2023, 1, 14), event=True, expand=True
    )
    print(events_fetched3[0].data)

# Больше примеров кода с CalDAV:
# https://github.com/python-caldav/caldav/tree/master/examples
