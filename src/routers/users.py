from fastapi import APIRouter, Security, Depends
from fastapi.security import OAuth2PasswordRequestForm

from crud.auth import (get_current_active_user, authenticate, get_token)
from crud.users import UsersCollection

router = APIRouter()

#  Route to add user to a particular organization
@router.post(
    "/user/register",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def register(
    password: str,
    email: str,
    name: str,
    organization_id: int,
    can_write: bool = False
):
    try:
        users_collection = UsersCollection()
        return await users_collection.register(password=password, email=email, name=name, can_write=can_write, organization_id=organization_id)
    except Exception as e:
        raise e
    
# Route to login user
@router.post("/user/login")
async def login_user(
    credentials: OAuth2PasswordRequestForm = Depends(),
):
    try:
        user = await authenticate(credentials)
        if user == False:
            return "User not found or something is wrong"

        access_token = await get_token(user=user)
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }
    except Exception as e:
        raise e

# Route to get user details for the particular user
@router.get(
    "/user/me",
    dependencies=[Security(get_current_active_user, scopes=["user:read"])],
)
async def read_user_me(
    current_user = Security(get_current_active_user,scopes=["user:read"])
):
    try:
        return current_user
    except Exception as e:
        raise e