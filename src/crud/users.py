from fastapi import HTTPException

from utils.master import (get_scope_list)
from crud.organizations import organizations

# Initiating Users Dictionary with a admin user
users = {
    "1": {
        "password": "12345",
        "username": "1",
        "email": "abhishekdwivedi131@gmail.com",
        "role": "admin",
        "permission": ["admin:read","admin:write","user:read","user:write"],
        "name": "Admin",
        "organization_id": 1
    },
}

# Username counter
username_count = 2

# Users Collection Class
class UsersCollection:
    def __init__(self):
        self.users = users
        self.username= username_count
    
    # Register CRUD Operation
    async def register(
        self, 
        password: str,
        email: str,
        name: str,
        can_write: bool,
        organization_id: int,
    ) -> any:
        try:
            # Checking if organization exists or not
            if organization_id not in organizations:
                return f"""Cant create user with organization_id:{organization_id}"""
            
            # creating user dictionary
            user = {
                "name": name,
                "username": str(self.username),
                "email": email,
                "role": "user",
                "password": password,
                "organization_id": organization_id
            }
            # get scope list for the user
            scopes = await get_scope_list(user=user, can_write=can_write)
            user["permission"] = scopes

            users[str(self.username)] = user

            # Incrementing the username counter
            global username_count
            username_count += 1

            # returning the created user
            return user
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")

