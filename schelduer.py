import os
from datetime import datetime, timedelta

import caldav
from dotenv import load_dotenv

load_dotenv()

caldav_url = os.getenv("CAL_URL")
username = os.getenv("CAL_USER")
password = os.getenv("CAL_PASS")

SCHELDUE_SUCCESS_MSG = "Вы успешно записались"

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
