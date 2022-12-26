from pydantic import BaseModel, validator
from users_session.utils_pass import get_hashed

from typing import Optional, Union


class Users(BaseModel):
    username: str
    name: str
    password:str

    @validator("rfi_id", allow_reuse=True)
    def formated_rf_id(cls,v):        
        return v.replace(" ", '')

    @validator("password", allow_reuse=True)
    def formated_rf_id(cls,v):
        return get_hashed(v)


class LoginUser(BaseModel):
    username: str
    password: str
