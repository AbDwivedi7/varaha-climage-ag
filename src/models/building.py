from pydantic import BaseModel

class BookingTimeSlot(BaseModel):
    start_time: int
    end_time: int