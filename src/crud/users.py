users = {
    "1": {
        "name": "Abhishek",
        "password": "12345",
        "username": "1",
        "is_admin": True
    },
}

users_id = 2

class UsersCollection:
    def __init__(self):
        self.users = users
        self.users_id = users_id
    
    def add_user(self, username) -> any:
        return None

