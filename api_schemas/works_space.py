from pydantic import BaseModel, root_validator
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId

class InfoUser(BaseModel):
    username: str
    name:str 
class InfoDocument(BaseModel):
    _id: ObjectId
    id: Optional[str]
    name: str
    size: int
    type: str
    time_create: datetime

    @root_validator(pre=True)
    def fix_id(cls, values):
        values['id'] = str(values["_id"])
        return values


class SettingDocument(BaseModel):
    setting_type: Optional[str] = "document"
    data: List[InfoDocument]


class WorkSpace(BaseModel):
    info_user: InfoUser
    all_setting: SettingDocument