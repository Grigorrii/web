from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi import Response, Header
from datetime import datetime, timezone, timedelta
from bson.objectid import ObjectId
import os, json, shutil

from setting_web import document_collection, head_conf

from models.document_model import DocumntMongoDocument
from .utils.counter_pages import counter_pages

from users_session.setting_token import check_user, ParsToken


router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/")
async def upload_new_file(data_documents: UploadFile = File(...),
                          Authorize: ParsToken = Depends(check_user)):

    if data_documents.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="dont correct type File. Only pdf")

    # Формируем путь до файла
    pathNewFile = f"{head_conf.file_name}/files/{str(Authorize.user_id)}/{data_documents.filename}"

    while True:
        try:
            with open(pathNewFile, "wb") as buffer:
                shutil.copyfileobj(data_documents.file, buffer)
            break
        except FileNotFoundError:
            os.mkdir(os.path.join(head_conf.file_name + "/files", str(Authorize.user_id)))

    size_page = await counter_pages(data_documents.file)
    new_obj_document = DocumntMongoDocument(user_id=Authorize.user_id, path=pathNewFile, name=data_documents.filename,
                                            type=data_documents.content_type, size=size_page,
                                            time_create=datetime.now(tz=timezone(timedelta(hours=3))))

    doc_mongo = document_collection.insert_one(
        json.loads(new_obj_document.json()))
    new_obj_document.id = str(doc_mongo.inserted_id)

    return JSONResponse(status_code=201, content=json.loads(new_obj_document.json(exclude={'_id'})))


@router.delete("/delete/")
async def drop_file(document_id: str, Authorize: ParsToken = Depends(check_user)):
    try:
        doc_info: DocumntMongoDocument = DocumntMongoDocument(
            **document_collection.find_one_and_delete({"_id": ObjectId(document_id)}))
        os.remove(doc_info.path)

        return JSONResponse(status_code=200, content={"message": "good delete"})
    except:
        return JSONResponse(status_code=400, content={"message": "bad delete"})

