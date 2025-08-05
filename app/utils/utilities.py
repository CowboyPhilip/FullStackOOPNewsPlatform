from passlib.context import CryptContext
from odmantic import ObjectId
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from typing import Any, Optional, Literal
from jose import jwt,JWTError,ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from app.config.config import TOKEN_PARAMS, settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def hashPassword(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_Object_id(id: str | ObjectId) -> bool:
    return ObjectId.is_valid(id)


def JsonRes(
    contentName: str,
    content: Any,
    statusCode: int,
    message: Optional[str | None] = None,
) -> JSONResponse:

    data = jsonable_encoder(content)
    response_data = {
        contentName: data,
        **({"message": message} if message is not None else {}),
    }

    return JSONResponse(content=response_data, status_code=statusCode)


def SignJwt(
    *,
    obj: dict[str, Any],
    expires_in: int,
    keyIdentifier: Literal["ACCESSTOKENPRIVATEKEY", "REFRESHTOKENPRIVATEKEY"]
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    to_encode = {"exp": expire, "user": obj}
    token = jwt.encode(to_encode, TOKEN_PARAMS[keyIdentifier], settings.JWT_ALGO)
    return token


# token = SignJwt(obj={"email":"omarsamir232@gmail.com",'id':12458586969},expires_in=900,keyIdentifier='ACCESSTOKENPRIVATEKEY')


def verifyJwt(
    *,
    token: str,
    keyIdentifier: Literal["ACCESSTOKENPUBLICKEY", "REFRESHTOKENPUBLICKEY"]
):
    try: 
       result =  jwt.decode(token, TOKEN_PARAMS[keyIdentifier], settings.JWT_ALGO)
    except ExpiredSignatureError:
        raise HTTPException(401,detail='token has expired')
    except JWTError:
        raise HTTPException(401,detail='error verifying jwt')
    else:
        return result


# print(verifyJwt(token=token,keyIdentifier='ACCESSTOKENPUBLICKEY'))
