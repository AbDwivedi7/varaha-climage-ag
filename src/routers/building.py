from fastapi import APIRouter, Security
from typing import Optional
from datetime import datetime

from crud.auth import (get_current_active_user)
from crud.building import BuildingCollection

from models.building import BookingTimeSlot

router = APIRouter()

# Route to get the building layout
@router.get(
    "/building/get_building",
    dependencies=[Security(get_current_active_user, scopes=["admin:read"])],
)
async def get_building():
    try:
        building_collection = BuildingCollection()
        return await building_collection.get_building()
    except Exception as e:
        raise e

# Route to add floor to the building
@router.get(
    "/building/add_floor",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_floor(
    floor_number: int
):
    try:
        building_collection = BuildingCollection()
        return await building_collection.add_floor(floor_number=floor_number)
    except Exception as e:
        raise e

# Route to add room to a particular floor
@router.get(
    "/building/add_room",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_room(
    floor_number: int,
    room_name: str,
    capacity: int,
    additional_details: Optional[dict] = None
):
    try:
        building_collection = BuildingCollection()
        return await building_collection.add_room(
            floor_number=floor_number,
            room_name=room_name,
            capacity=capacity,
            additional_details=additional_details
        )
    except Exception as e:
        raise e


#  Route to get all available rooms to next 24 Hours
@router.get(
    "/building/get_conference_rooms",
    dependencies=[Security(get_current_active_user, scopes=["user:read"])],
)
async def get_conference_rooms():
    try:
        building_collection = BuildingCollection()
        return await building_collection.get_conference_rooms()
    except Exception as e:
        print("router", e)
        raise e

# Route to get specified rooms for datetime, capacity or suggested rooms
@router.post(
    "/building/get_suitable_conference_rooms",
    dependencies=[Security(get_current_active_user, scopes=["user:read"])],
)
async def get_suitable_conference_rooms(
    capacity: Optional[int] = 0,
    equipment_available: Optional[dict] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    try:
        building_collection = BuildingCollection()
        return await building_collection.get_suitable_conference_rooms(
            capacity=capacity,
            equipment_available=equipment_available,
            start_time=start_time,
            end_time=end_time
        )
    except Exception as e:
        raise e
