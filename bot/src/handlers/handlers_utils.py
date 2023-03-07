from app import user_service_v1
from core.constants import MeetingFormat
from handlers.meeting import buttons
from schemas.responses import MeetingResponse


def make_message_for_active_meeting(user_active_meeting: list[MeetingResponse]) -> str:
    meeting_obj = user_active_meeting[0]
    meeting_time = meeting_obj.date_start
    meeting_format = (
        buttons.BTN_MEETING_FORMAT_ONLINE.text
        if meeting_obj.format == MeetingFormat.MEETING_FORMAT_ONLINE
        else buttons.BTN_MEETING_FORMAT_OFFLINE.text
    )
    ps = user_service_v1.get_user(id=meeting_obj.psychologist)
    text = (
        f"У вас уже имеется активная запись:\n"
        f"Психолог: {ps.first_name} {ps.last_name}\n"
        f"Когда: {meeting_time}\n"
        f"Формат: {meeting_format}"
    )
    return text
