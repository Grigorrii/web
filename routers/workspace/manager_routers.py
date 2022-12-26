from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import Header
from bson.objectid import ObjectId
from typing import Union
import os
import json

from setting_web import document_collection, users_collection, head_conf

from users_session.setting_token import ParsToken, check_user
from api_schemas.works_space import WorkSpace, InfoUser, InfoDocument, SettingDocument

router = APIRouter(prefix="/workspace", tags=["Workspace"])


@router.get("/", response_model=WorkSpace)
async def upload_new_file(Authorize: ParsToken = Depends(check_user)):
    objUserID = Authorize.user_id

    try:
        settingUser = InfoUser(**users_collection.find_one({"_id": ObjectId(objUserID)}))
    except TypeError:
        raise HTTPException(status_code=404, detail="user not find")

    docUser = list(map(lambda x: InfoDocument(**x), document_collection.find({"user_id": objUserID})))
    settingDoc = SettingDocument(data=docUser)
    
    return JSONResponse(status_code=200, content=json.loads(WorkSpace(info_user=settingUser, all_setting=settingDoc).json()))
