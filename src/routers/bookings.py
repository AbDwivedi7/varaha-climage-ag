from fastapi import APIRouter, Security, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

from crud.auth import (get_current_active_user)
from crud.bookings import BookingsCollection

router = APIRouter()

@router.get(
    "/booking/book",
    dependencies=[Security(get_current_active_user, scopes=["user:write"])],
)
async def book(
    room_id: int,
    floor_number: int,
    start_time: datetime,
    end_time: datetime,
    current_user = Security(get_current_active_user,scopes=["user:read"])
):
    try:
        bookings_collection = BookingsCollection()
        return await bookings_collection.book_conference_room(
            room_id=room_id,
            floor_number=floor_number,
            start_time=start_time,
            end_time=end_time,
            current_user = current_user
        )
    except Exception as e:
        raise e

@router.get(
    "/booking/get_all_bookings",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def book():
    try:
        bookings_collection = BookingsCollection()
        return await bookings_collection.get_all_bookings()
    except Exception as e:
        return e