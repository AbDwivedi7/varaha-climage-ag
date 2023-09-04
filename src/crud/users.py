from utils.master import (get_scope_list)

users = {
    "1": {
        "password": "12345",
        "username": "1",
        "email": "abhishekdwivedi131@gmail.com",
        "role": "admin",
        "permission": ["admin:read","admin:write","user:read","user:write"],
        "name": "Admin",
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
        can_write: bool
    ) -> any:
        try:
            user = {
                "name": name,
                "username": str(self.username),
                "email": email,
                "role": "user",
                "password": password
            }
            scopes = await get_scope_list(user=user, can_write=can_write)
            user["permission"] = scopes

            users[str(self.username)] = user

            global username_count
            username_count += 1

            return user
        except Exception as e:
            return e

