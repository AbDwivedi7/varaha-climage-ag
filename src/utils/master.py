from datetime import datetime, timedelta

from models.building import BookingTimeSlot

from utils.data import bookings

async def get_scope_list(
    user: dict,
    can_write: bool
):
    if user["role"] == "admin":
        scopes = [
            "admin:read",
            "admin:write",
            "user:read",
            "user:write",
        ]
    elif user["role"] == "user" and can_write:
        scopes = [
            "user:read",
            "user:write",
        ]
    else:
        scopes = [
            "user:read",
        ]
    return scopes

async def convert_to_datetime(date_str: str, time_slot: BookingTimeSlot) -> (datetime, datetime):
    start_time_str = f"{date_str} {time_slot.start_time}:00"
    end_time_str = f"{date_str} {time_slot.end_time}:00"
    format_str = "%Y-%m-%d %H:%M"
    start_time = datetime.strptime(start_time_str, format_str)
    end_time = datetime.strptime(end_time_str, format_str)
    return start_time, end_time

async def get_date_difference_in_hours(start_time: datetime, end_time: datetime) -> int:
    duration = end_time - start_time
    duration_in_second = duration.total_seconds()
    return int(duration_in_second // 3600)

async def check_room_availability(room_id, start_time, end_time):
    try:
        start_time = start_time + timedelta(seconds=1)
        end_time = end_time - timedelta(seconds=1)

        for booking in bookings:
            if booking["room_id"] == room_id:
                if  (start_time < booking["end_time"] and start_time > booking["start_time"] ) or (end_time < booking["end_time"] and end_time > booking["start_time"] ):
                    return False
        return True
    except Exception as e:
        return e