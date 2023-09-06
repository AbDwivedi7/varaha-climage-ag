from fastapi import HTTPException
from datetime import datetime
from typing import Optional
import threading

from utils.master import convert_to_datetime, check_room_availability, get_date_difference_in_hours
from utils.data import building
from models.bookings import Booking

from utils.data import bookings, monthly_booking_hours, booking_id_count

lock = threading.Lock()

class BookingsCollection:
    def __init__(self):
        self.bookings = bookings
        self.monthly_booking_hours = monthly_booking_hours
        self.booking_id_count = booking_id_count

    async def book_conference_room(
        self,
        room_id: int,
        floor_number: int,
        start_time: datetime,
        end_time: datetime,
        current_user: dict
    ):
        try:
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
                                "id": self.booking_id_count,
                                "room_id": room_id,
                                "room_name": room["name"],
                                "floor_number": floor_number,
                                "start_time": start_time,
                                "end_time": end_time,
                                "booked_by": current_user["username"],
                                "organization_id": current_user["organization_id"],
                                "status": "booked"
                            }
                            with lock:
                                self.bookings.append(booking)
                            self.monthly_booking_hours[month_key] = already_booked_hours+current_booking_hours                   
                            global booking_id_count
                            booking_id_count += 1

                            return {"message": "Room booked successfully."}
            return "Not found"
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")
    

    async def get_all_bookings(self):
        try:
            with lock:
                return self.bookings
        except Exception as e:
            raise HTTPException(status_code=400, detail="Something went wrong")
    
    async def cancel_booking(
        self,
        booking_id: int,
        current_user: dict
    ):
        try:
            with lock:
                for booking in self.bookings:
                    if booking["id"] == booking_id and current_user["organization_id"] == booking["organization_id"]:
                        booking["status"] = "cancelled"
                        booking["cancelled_by"] = current_user["username"]
                        return "Booking Cancelled"
            
            return "Booking not found"
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")
    
    async def get_all_organization_bookings(
        self,
        current_user: dict,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        try:
            all_organization_booking = []
            with lock:
                for booking in self.bookings:
                    if start_date != None and end_date != None and start_date < end_date:
                        if current_user["organization_id"] == booking["organization_id"] and booking["start_time"] >= start_date and booking["end_time"] <= end_date:
                            all_organization_booking.append(booking)
                    else:
                        if current_user["organization_id"] == booking["organization_id"]:
                            all_organization_booking.append(booking)
            
            return all_organization_booking
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")
    
    async def get_all_user_bookings(
        self,
        username: int,
        current_user: dict,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        try:
            all_organization_booking = []
            with lock:
                for booking in self.bookings:
                    if start_date != None and end_date != None and start_date < end_date:
                        if current_user["organization_id"] == booking["organization_id"] and booking["start_time"] >= start_date and booking["end_time"] <= end_date and booking["booked_by"] == str(username):
                            all_organization_booking.append(booking)
                    else:
                        if current_user["organization_id"] == booking["organization_id"] and booking["booked_by"] == str(username):
                            all_organization_booking.append(booking)
            
            return all_organization_booking
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")