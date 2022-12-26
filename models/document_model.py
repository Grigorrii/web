from pydantic import BaseModel, root_validator
from typing import Optional

from datetime import datetime


class DocumntMongoDocument(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    name: Optional[str] = "undefined_doc"
    size: Optional[int]
    type: Optional[str]
    path: Optional[str]
    time_create: Optional[datetime]
    
    @root_validator(pre=True)
    def fix_id(cls, values):
        if values.get("_id") is None:
            return values

        values['id'] = str(values["_id"])
        return values
