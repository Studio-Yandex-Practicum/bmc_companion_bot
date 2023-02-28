from dataclasses import dataclass

from request.services import PydanticApiService
from schemas.responses import MeetingResponse, TimeslotResponse


@dataclass
class ScheduleApiService(PydanticApiService):
    url_timeslots = "timeslots/"
    url_meetings = "meetings/"

    def get_actual_timeslots(self, **kwargs) -> list[TimeslotResponse]:
        return self.get(TimeslotResponse, self.url_timeslots, params=kwargs)

    def get_meetings_by_user(self, **kwargs) -> MeetingResponse | list[MeetingResponse]:
        return self.get(MeetingResponse, self.url_meetings, params=kwargs)

    def create_meeting(
        self, psychologist_id: int, user_id: int, comment: str, date_start, meeting_format
    ) -> MeetingResponse:
        data = {
            "psychologist": psychologist_id,
            "user": user_id,
            "comment": comment,
            "date_start": date_start,
            "format": meeting_format,
        }
        return self.post(MeetingResponse, self.url_meetings, data=data)

    def update_meeting(
        self, psychologist_id: int, user_id: int, date_start, meeting_format, meeting_id
    ) -> MeetingResponse:
        data = {
            "psychologist": psychologist_id,
            "user": user_id,
            "date_start": date_start,
            "format": meeting_format,
            "meeting_id": meeting_id,
        }
        return self.patch(MeetingResponse, self.url_meetings + str(meeting_id) + "/", data=data)

    def delete_meeting(self, meeting_id) -> MeetingResponse:
        return self.delete(MeetingResponse, self.url_meetings + str(meeting_id))
