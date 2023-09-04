from pydantic import BaseModel

from models.building import BookingTimeSlot

class Booking(BaseModel):
    room_name: str
    floor: int
    date: str
    time_slot: BookingTimeSlot