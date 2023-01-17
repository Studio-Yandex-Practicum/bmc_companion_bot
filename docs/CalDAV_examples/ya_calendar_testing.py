import os
from datetime import datetime

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

# Встроенный метод поиска по датам.
events_fetched = ya_calendar.search(
    start=datetime(2022, 12, 20), end=datetime(2022, 12, 21), event=True, expand=True
)

# Получение всех данных о событии.
# print(events_fetched[0].data)


# event = events_fetched[0]

# Альтернативный метод поиска по uid.
# uid_event = ya_calendar.event_by_uid(uid="X7MyHOeoyandex.ru")

# Примеры параметров, по которым можно фильтровать события.
# event.vobject_instance.vevent.summary.value == "Слот1"
# event.vobject_instance.vevent.transp.value == "OPAQUE"
# event.vobject_instance.vevent.url.value == (
#    "https://calendar.yandex.ru/event?event_id=1796961824"
# )
# event.vobject_instance.vevent.categories.value == ['Testing']
# event.vobject_instance.vevent.uid.value == "X7MyHOeoyandex.ru"


# Параметры относящиеся к дате события:
# event.vobject_instance.vevent.dtstart.value
# event.vobject_instance.vevent.dtend.value
# event.vobject_instance.vevent.dtstamp.value
# event.vobject_instance.vevent.created.value
# event.vobject_instance.vevent.last_modified.value

# Пример фильтрации по саммари и последующего удаления события.
for event in ya_calendar.events():
    if event.vobject_instance.vevent.summary.value == "Слот1":
        print(f"Событие найдено, его uid {event.vobject_instance.vevent.uid.value}")
        event.delete()

# Добавление нового ивента.
# ya_calendar.save_event(
#         dtstart=datetime(2022, 12, 26, 12),
#         dtend=datetime(2022, 12, 26, 13),
#         summary="Слот 1",
#     )

# Больше примеров кода с CalDAV:
# https://github.com/python-caldav/caldav/tree/master/examples
