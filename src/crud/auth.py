
from fastapi.security import (OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes)
from fastapi import Depends, HTTPException, status
from datetime import timedelta, datetime
import jwt
from jwt import PyJWTError
from pydantic import BaseModel, ValidationError
from typing import List, Optional

from crud.users import (users)
from models.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 3600 # Token Expiration in minutes
ALGORITHM = "HS256" # Algorithm for encoding/decoding JWT Token
JWT_SECRET_KEY = "123456789" # Key used for JWS Secret Key for encoding/decoding JWT Token 

# Authenticating user based on username and password
async def authenticate(credentials: OAuth2PasswordRequestForm):
    user = users[credentials.username]
    if not user:
        return False
    if credentials.password != user["password"]:
        return False
    return user


# Getting current logged in user
async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    try:
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = f"Bearer"

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("username")
            if username is None:
                raise credentials_exception

            token_scopes = payload.get("scopes", [])
            token_data = TokenData(username=username, scopes=token_scopes)
        except (PyJWTError, ValidationError):
            raise credentials_exception

        if token_data.username not in users:
            raise credentials_exception
        
        user = users[token_data.username]

        if user is None:
            raise credentials_exception

        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
        return user
    except Exception as e:
        raise e


# Wrapper function to get active user
async def get_current_active_user(
    current_user= Depends(get_current_user),
):
    return current_user if current_user else "Not Found"

# Generating JWT Token
async def get_token(
    user: dict,
):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "username": user["username"],
            "scopes": user["permission"],
        },
        expires_delta=access_token_expires,
    )
    return access_token


# Creating access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt