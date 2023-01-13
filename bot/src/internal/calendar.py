from datetime import datetime, timedelta
from typing import Type, TypeVar

import caldav
from internal.exceptions import CalendarRequestError
from pydantic import UserFull

ModelType = TypeVar("ModelType", bound=UserFull)


class Calendar:
    def __init__(self, psychologist: Type[ModelType]) -> None:
        self.psychologist = psychologist

    def connect(self):
        caldav_url = self.psychologist.psychologist_info.cal_link
        username = self.psychologist.psychologist_info.cal_username
        password = self.psychologist.psychologist_info.cal_pass

        client = caldav.DAVClient(url=caldav_url, username=username, password=password)
        my_principal = client.principal()
        calendars = my_principal.calendars()
        calendar = calendars[0]
        try:
            assert calendar
        except caldav.error.NotFoundError as e:
            raise CalendarRequestError(f"Соединения с календарем нет {e}")
        return calendar

    def get_events(self, date_a: datetime.date, date_b: datetime.date):
        calendar = self.connect
        events_fetched = calendar.search(start=date_a, end=date_b, event=True, expand=True)
        return events_fetched

    def add_event(self, date_start, summary):
        calendar = self.connect
        calendar.save_event(
            dtstart=date_start,
            dtend=(date_start + timedelta(hours=1)),
            dtstamp=datetime.now(),
            summary=f"{summary}",
        )
