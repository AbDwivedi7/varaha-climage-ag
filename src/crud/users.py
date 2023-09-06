from fastapi import HTTPException

from utils.master import (get_scope_list)
from crud.organizations import organizations

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

username_count = 2

class UsersCollection:
    def __init__(self):
        self.users = users
        self.username= username_count
    
    async def register(
        self, 
        password: str,
        email: str,
        name: str,
        can_write: bool,
        organization_id: int,
    ) -> any:
        try:
            if organization_id not in organizations:
                return f"""Cant create user with organization_id:{organization_id}"""
            
            user = {
                "name": name,
                "username": str(self.username),
                "email": email,
                "role": "user",
                "password": password,
                "organization_id": organization_id
            }
            scopes = await get_scope_list(user=user, can_write=can_write)
            user["permission"] = scopes

            users[str(self.username)] = user

            global username_count
            username_count += 1

            return user
        except Exception:
            raise HTTPException(status_code=400, detail="Something went wrong")

