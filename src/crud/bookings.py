from fastapi import HTTPException
from datetime import datetime

from utils.master import convert_to_datetime, check_room_availability
from utils.data import building
from models.bookings import Booking

from utils.data import bookings

class BookingsCollection:
    def __init__(self):
        pass

    async def book_conference_room(
        room_id: int,
        floor_number: int,
        start_time: datetime,
        end_time: datetime,
        current_user: dict
    ):
        try:
            for floor, rooms in building:
                if floor == floor_number:
                    for room in rooms:
                        if room["id"] == room_id:
                            already_booked = await check_room_availability(room_id=room_id, start_time=start_time, end_time=end_time)
                            if already_booked:
                                raise HTTPException(
                                    status_code=400,
                                    detail="The room is not available for the selected time."
                                )
                            booking = {
                                "room_id": room_id,
                                "room_name": room["name"],
                                "floor_number": floor_number,
                                "start_time": start_time,
                                "end_time": end_time,
                                "booked_by": current_user["username"],
                                "organization_id": current_user["organization_id"]
                            }
                            bookings.append(booking)
                            return {"message": "Room booked successfully."}
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")
    
