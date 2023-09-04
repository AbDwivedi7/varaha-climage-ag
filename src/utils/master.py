from datetime import datetime

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


async def check_room_availability(room_name, start_time, end_time):
    for booking in bookings:
        if booking["room"] == room_name:
            booking_start, booking_end = await convert_to_datetime(booking["date"], booking["time_slot"])
            if  start_time < booking_end and end_time > booking_start :
                return False
    return True