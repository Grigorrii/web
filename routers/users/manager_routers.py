from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
from pymongo.errors import DuplicateKeyError
from setting_web import head_conf

from .users_shemas import Users, LoginUser
from users_session.setting_token import AuthJWT, SettingsJWT, check_user, ParsToken
from users_session.utils_pass import verify_password, authenticate_user, create_token
from models.users_model import UserDocument
from api_schemas.authorization import AuthorizationSchema

import json
from setting_web import users_collection

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=AuthorizationSchema)
async def create_users(data_user: Users, Authorize: AuthJWT = Depends()):
    try:
        student = users_collection.insert_one(json.loads(data_user.json()))
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="this user exits")

    get_tocken: AuthorizationSchema = await create_token(UserDocument(id=str(student.inserted_id)))
    return JSONResponse(status_code=200,  content=json.loads(get_tocken.json()))


@ router.delete("/logout")
async def logout(Authorize: ParsToken = Depends(check_user)):
    print(Authorize)

    head_conf.jwt_block_list.setex(
        Authorize.jti, SettingsJWT().access_expires, 1)
    return JSONResponse(status_code=200, content={"message": "logout good"})


@router.post("/login")
async def login_user(data_user: LoginUser):
    find_users = users_collection.find_one({"username": data_user.username})

    if find_users:
        user_doc = UserDocument(**find_users)
        status_verfy = verify_password(data_user.password, user_doc.password)

        if status_verfy:
            get_tocken: AuthorizationSchema = await create_token(user_doc)
            return JSONResponse(status_code=200,  content=json.loads(get_tocken.json()))
        else:
            raise HTTPException(status_code=401, detail="this user exits")
    else:
        raise HTTPException(status_code=404, detail="dont find Users")


@router.post("/token/", response_model=AuthorizationSchema)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), Authorize: AuthJWT = Depends()):
    user_doc = await authenticate_user(form_data.username, form_data.password)
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    get_tocken: AuthorizationSchema = await create_token(user_doc)
    return JSONResponse(status_code=200,  content=json.loads(get_tocken.json()))
