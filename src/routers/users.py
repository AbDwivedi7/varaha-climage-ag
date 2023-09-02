from fastapi import APIRouter, Security, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from crud.auth import (get_current_active_user, authenticate, get_token)

router = APIRouter()


@router.post(
    "/user/register",
    dependencies=[Security(get_current_active_user, scopes=["admin:write"])],
)
async def register(user: dict):
    try:
        print(user)
        return True
    except Exception as e:
        return e
    
@router.post("/user/login")
async def login_user(
    credentials: OAuth2PasswordRequestForm = Depends(),
):
    try:
        user, scopes = await authenticate(credentials)
        if user == False:
            return "User not found or something is wrong"

        access_token = await get_token(user=user, scopes=scopes)
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }
    except Exception as e:
        return e

@router.get(
    "/user/me",
    dependencies=[Security(get_current_active_user, scopes=["guest:read"])],
)
async def read_user_me(
    current_user = Security(get_current_active_user,scopes=["guest:read"],)
):
    try:
        return current_user
    except Exception as e:
        raise e