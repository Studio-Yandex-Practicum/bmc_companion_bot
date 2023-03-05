from dataclasses import dataclass
from urllib.parse import urljoin

from request.services import PydanticApiService
from schemas.responses import FeedbackResponse, MeetingResponse, TimeslotResponse


@dataclass
class ScheduleApiService(PydanticApiService):
    url_timeslots = "timeslots/"
    url_meetings = "meetings/"
    url_feedbacks = "meeting_feedbacks/"

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

    def create_feedback(
        self, meeting_id: int, user_id: int, text: str, score: int
    ) -> FeedbackResponse:
        data = {
            "meeting": meeting_id,
            "user": user_id,
            "text": text,
            "score": score,
        }
        return self.post(FeedbackResponse, self.url_feedbacks, data=data)

    def update_feedback(self, feedback_id: int, **kwargs) -> FeedbackResponse:
        return self.patch(
            FeedbackResponse,
            urljoin(self.url_feedbacks, f"{feedback_id}/"),
            data=kwargs,
        )

    def get_feedback_by_user_and_meeting(
        self, **kwargs
    ) -> FeedbackResponse | list[FeedbackResponse] | None:
        return self.get(FeedbackResponse, self.url_feedbacks, params=kwargs)
