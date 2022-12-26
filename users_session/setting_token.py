from pydantic import BaseModel, Field
from datetime import timedelta
from typing import Optional

from setting_web import head_conf, app, reuseable_oauth

from fastapi import Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException


class SettingsJWT(BaseModel):
    authjwt_secret_key: str = head_conf.SECRET_KEY
    authjwt_denylist_enabled: bool = True
    # authjwt_denylist_token_checks: set = {"access","refresh"}
    authjwt_algorithm: str = head_conf.ALGORITHM
    access_expires: int = timedelta(minutes=30)
    refresh_expires: int = timedelta(days=30)


class ParsToken(BaseModel):
    user_id: str = Field(alias='sub')
    jti: str


@AuthJWT.load_config
def get_config():
    return SettingsJWT()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    token_in_redis = head_conf.red.get(jti)
    return token_in_redis is not None


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

async def check_user(auth: AuthJWT = Depends(), token: str = Depends(reuseable_oauth)) -> ParsToken:
    auth.jwt_required()
    return ParsToken(**auth.get_raw_jwt())


