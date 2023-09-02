from fastapi import APIRouter, Security
from typing import Optional

from crud.auth import (get_current_active_user)
from crud.building import BuildingCollection

router = APIRouter()

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

@router.get(
    "/building/add_room",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def add_room(
    floor_number: int,
    room_name: str,
    capacity: str,
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

