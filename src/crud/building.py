from datetime import date, datetime, timedelta
from typing import Optional

from models.building import BookingTimeSlot
from utils.master import check_room_availability
from utils.data import building, bookings, room_id


class BuildingCollection:
    def __init__(self):
        self.building = building
        self.room_id = room_id
    
    async def get_building(self):
        try:
            return self.building
        except Exception as e:
            return e
       

    async def add_floor(self, floor_number):
        try:
            if floor_number not in self.building:
                self.building[floor_number] = []
                return f"""{floor_number} floor added"""
            return f"""{floor_number} floor already exists"""
        except Exception as e:
            return e

    async def add_room(self, floor_number, room_name, capacity: int, additional_details=None):
        try:
            if floor_number not in self.building:
                return f"Floor {floor_number} does not exist. Create the floor first."

            room = {
                "id": self.room_id,
                "name": room_name,
                "capacity": capacity,
                "floor_number": floor_number
            }

            if additional_details:
                room["Additional Details"] = additional_details

            self.building[floor_number].append(room)

            global room_id
            room_id += 1

            return {"floor_number": floor_number, "room_details": room}
        except Exception as e:
            return e
    
    async def get_conference_rooms(self):
        try:
            available_rooms = {}
            current_time = datetime.now()
            current_time = current_time.replace(minute=0, second=0, microsecond=0)

            stop_time = datetime.now()
            stop_time = stop_time.replace(hour=0,minute=0, second=0, microsecond=0)
            stop_time = stop_time + timedelta(days=1)
            
            for _, rooms, in building.items():
                for room in rooms:
                    available_room_slot = []
                    next_hour_start = current_time + timedelta(hours=1)
                    next_hour_end = current_time + timedelta(hours=2)
                    while next_hour_end <= stop_time:
                        is_available = await check_room_availability(room["id"], next_hour_start, next_hour_end)
                        if is_available:
                            available_room_slot.append([next_hour_start, next_hour_end])
                            
                        next_hour_start = next_hour_end
                        next_hour_end = next_hour_end + timedelta(hours=1)
                    available_rooms[room["id"]] = {
                        "details": room,
                        "slots": available_room_slot
                    }
            return available_rooms
        except Exception as e:
            return e

    
    async def get_suitable_conference_rooms(
        self,
        capacity: Optional[int] = 0,
        equipment_available: Optional[dict] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        try:
            if capacity == 0 and (equipment_available == None or equipment_available == {}) and start_time == None and end_time == None:
                return self.get_conference_rooms()
            
            available_rooms = {}
            for _, rooms, in building.items():
                for room in rooms:
                    if start_time != None and end_time != None and room["capacity"] >= capacity:
                        is_available = await check_room_availability(room["id"], start_time, end_time)
                        if is_available:
                            available_rooms[room["id"]] = {
                                "details": room,
                                "slots": [start_time, end_time]
                            }
                    elif room["capacity"] >= capacity:
                        current_time = datetime.now()
                        current_time = current_time.replace(minute=0, second=0, microsecond=0)

                        stop_time = datetime.now()
                        stop_time = stop_time.replace(hour=0,minute=0, second=0, microsecond=0)
                        stop_time = stop_time + timedelta(days=1)

                        available_room_slot = []
                        next_hour_start = current_time + timedelta(hours=1)
                        next_hour_end = current_time + timedelta(hours=2)
                        while next_hour_end <= stop_time:
                            is_available = await check_room_availability(room["id"], next_hour_start, next_hour_end)
                            if is_available:
                                available_room_slot.append([next_hour_start, next_hour_end])
                            next_hour_start = next_hour_end
                            next_hour_end = next_hour_end + timedelta(hours=1)

                        available_rooms[room["id"]] = {
                            "details": room,
                            "slots": available_room_slot
                        }
            
            return available_rooms
        except Exception as e:
            print(e, "get_suitable_conference_rooms")
            return e