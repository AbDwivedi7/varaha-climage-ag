from fastapi import HTTPException
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
    
    async def get_conference_rooms(
        self,
        start_time: Optional[datetime] = None,
        time_till: Optional[int] = 1,
        max_suggestions: Optional[int] = 0,
        capacity: Optional[int] = 0
    ):
        try:
            available_rooms = {}
            if start_time == None:
                current_time = datetime.now()
            else:
                current_time = start_time
            
            current_time = current_time.replace(minute=0, second=0, microsecond=0)

            stop_time = datetime.now()
            stop_time = stop_time.replace(minute=0, second=0, microsecond=0)
            stop_time = stop_time + timedelta(days=time_till)

            for _, rooms, in building.items():
                for room in rooms:
                    available_room_slot = []
                    next_hour_start = current_time + timedelta(hours=1)
                    next_hour_end = current_time + timedelta(hours=2)
                    while next_hour_end <= stop_time:
                        is_available = await check_room_availability(room["id"], next_hour_start, next_hour_end)
                        if is_available and room["capacity"]>=capacity:
                            available_room_slot.append([next_hour_start, next_hour_end])
                            
                        next_hour_start = next_hour_end
                        next_hour_end = next_hour_end + timedelta(hours=1)
                    
                    if len(available_room_slot) > 0:
                        available_rooms[room["id"]] = {
                            "details": room,
                            "slots": available_room_slot
                        }
            if max_suggestions == 0:
                return available_rooms
            else:
                return {k: available_rooms[k] for k in list(available_rooms)[:2]}
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
            print("get_suitable_conference_rooms hrer 1")
            if capacity == 0 and (equipment_available == None or equipment_available == {}) and start_time == None and end_time == None:
                return await self.get_conference_rooms()
            
            available_rooms = {}

            for _, rooms, in building.items():
                for room in rooms:
                    if start_time != None and end_time != None and start_time > datetime.now() and end_time > datetime.now() and room["capacity"] >= capacity:
                        is_available = await check_room_availability(room["id"], start_time, end_time)
                        if is_available:
                            available_rooms[room["id"]] = {
                                "details": room,
                                "slots": [start_time, end_time]
                            }
                    
                    elif room["capacity"] >= capacity:
                        if start_time == None:
                            current_time = datetime.now()
                        else:
                            current_time = start_time
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

                        if len(available_room_slot) > 0:
                            available_rooms[room["id"]] = {
                                "details": room,
                                "slots": available_room_slot
                            }
            
            if len(available_rooms) > 0:
                return {"available_room": available_rooms, "suggested_rooms": {}}
            else:
                suggested_room =  await self.get_conference_rooms(start_time=start_time if start_time != None else datetime.now(), time_till=3, max_suggestions=10, capacity=capacity)
                return {"available_room": {}, "suggested_rooms": suggested_room}
            
        except Exception as e:
            return e