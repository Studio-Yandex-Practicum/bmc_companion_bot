from dataclasses import dataclass

from request.services import PydanticApiService
from schemas.responses import MeetingResponse, TimeslotResponse


@dataclass
class ScheduleApiService(PydanticApiService):
    url_timeslots = "timeslots/"
    url_meetings = "meetings/"

    def get_actual_timeslots(self, is_free: str = "False", **kwargs) -> list[TimeslotResponse]:
        return self.get(TimeslotResponse, self.url_timeslots, params={**kwargs, "is_free": is_free})

    def get_meetings_by_user(
        self, is_active: str = "False", **kwargs
    ) -> MeetingResponse | list[MeetingResponse]:
        return self.get(
            MeetingResponse, self.url_meetings, params={**kwargs, "is_active": is_active}
        )

    def create_meeting(
        self, psychologist_id: int, user_id: int, comment: str, date_start, meeting_format, timeslot
    ) -> MeetingResponse:
        data = {
            "psychologist": psychologist_id,
            "user": user_id,
            "comment": comment,
            "date_start": date_start,
            "format": meeting_format,
            "timeslot": timeslot,
        }
        return self.post(MeetingResponse, self.url_meetings, data=data)
