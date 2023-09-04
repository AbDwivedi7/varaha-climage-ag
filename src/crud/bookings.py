from fastapi import HTTPException
from datetime import datetime

from utils.master import convert_to_datetime, check_room_availability, get_date_difference_in_hours
from utils.data import building
from models.bookings import Booking

from utils.data import bookings, monthly_booking_hours

class BookingsCollection:
    def __init__(self):
        self.bookings = bookings
        self.monthly_booking_hours = monthly_booking_hours

    async def book_conference_room(
        self,
        room_id: int,
        floor_number: int,
        start_time: datetime,
        end_time: datetime,
        current_user: dict
    ):
        try:
            print(room_id, floor_number, start_time, end_time, current_user)
            if start_time < datetime.now() or end_time < datetime.now():
                return "Cant book in the past"
            for floor, rooms in building.items():
                if floor == floor_number:
                    for room in rooms:
                        if room["id"] == room_id:
                            month_key = f"""{start_time.month}_{start_time.year}_{current_user["organization_id"]}"""

                            if month_key in self.monthly_booking_hours:
                                already_booked_hours = self.monthly_booking_hours[month_key]
                            else:
                                already_booked_hours = 0
                            current_booking_hours = await get_date_difference_in_hours(start_time=start_time, end_time=end_time)
                            if already_booked_hours+current_booking_hours > 30:
                                return "Cant book for more than 30 hours a month"
                            
                            is_available = await check_room_availability(room_id=room_id, start_time=start_time, end_time=end_time)
                            if not is_available:
                                return "Already booked"
                            
                            booking = {
                                "room_id": room_id,
                                "room_name": room["name"],
                                "floor_number": floor_number,
                                "start_time": start_time,
                                "end_time": end_time,
                                "booked_by": current_user["username"],
                                "organization_id": current_user["organization_id"]
                            }

                            self.bookings.append(booking)
                            self.monthly_booking_hours[month_key] = already_booked_hours+current_booking_hours                   

                            return {"message": "Room booked successfully."}
            return "Not found"
        except Exception as e:
            raise HTTPException(status_code=400, detail="Something went wrong")
    

    async def get_all_bookings(self):
        try:
            return self.bookings
        except Exception as e:
            raise HTTPException(status_code=400, detail="Something went wrong") 