from fastapi import HTTPException

from utils.master import convert_to_datetime
from utils.data import building
from models.bookings import Booking

from utils.data import bookings

class BookingsCollection:
    def __init__(self):
        pass

    async def book_conference_room(booking: Booking):
        try:
            start_time, end_time = convert_to_datetime(booking.date, booking.time_slot)
            for floor, rooms in building:
                if floor == booking.floor:
                    for room in rooms:
                        if room.name == booking.room_name:
                            for existing_booking in bookings:
                                existing_start, existing_end = convert_to_datetime(
                                    existing_booking.date, existing_booking.time_slot
                                )
                                if (
                                    existing_booking.room_name == room.name and
                                    start_time < existing_end and
                                    end_time > existing_start
                                ):
                                    raise HTTPException(
                                        status_code=400,
                                        detail="The room is not available for the selected time."
                                    )
                            bookings.append(booking)
                            return {"message": "Room booked successfully."}
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")