from pydantic import BaseModel, root_validator
from typing import Optional

class UserDocument(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = "undefined"
    name: Optional[str] = "undefined"
    password: Optional[str] = None

    @root_validator(pre=True)
    def fix_id(cls, values):
        if values.get("_id") is None:
            return values

        values['id'] = str(values["_id"])
        values['name'] = values['username']
        return values
