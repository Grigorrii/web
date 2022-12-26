from setting_web import password_context, head_conf, users_collection
from .setting_token import AuthJWT

from datetime import datetime, timedelta
from typing import Union, Any
from datetime import datetime
from models.users_model import UserDocument
from api_schemas.authorization import AuthorizationSchema

from fastapi import Depends


def get_hashed(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


async def authenticate_user(username: str, password: str):
    user = users_collection.find_one({"username": username})

    if not user:
        return False

    user = UserDocument(**user)
    if not verify_password(password, user.password):
        return False

    return user


async def create_token(user_doc: UserDocument) -> AuthorizationSchema:
    auth = AuthJWT()

    access_token = auth.create_access_token(subject=user_doc.id)
    refresh_token = auth.create_refresh_token(subject=user_doc.id)

    return AuthorizationSchema(access_token=access_token,
                               refresh_token=refresh_token)
