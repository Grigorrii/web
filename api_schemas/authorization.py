from pydantic import BaseModel, root_validator
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId


class AuthorizationSchema(BaseModel):
    access_token: str
    refresh_token: str
