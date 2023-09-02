building = {}

class BuildingCollection:
    def __init__(self):
        self.building = building
    
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

    async def add_room(self, floor_number, room_name, capacity, additional_details=None):
        try:
            if floor_number not in self.building:
                return f"Floor {floor_number} does not exist. Create the floor first."

            room = {
                "Room Name": room_name,
                "Capacity": capacity,
            }

            if additional_details:
                room["Additional Details"] = additional_details

            self.building[floor_number].append(room)

            return {"floor_number": floor_number, "room_details": room}
        except Exception as e:
            return e
    
