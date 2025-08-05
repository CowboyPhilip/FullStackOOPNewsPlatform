from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request,HTTPException
from app.utils.utilities import verifyJwt
from jose import JWTError,ExpiredSignatureError


class Auth(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        authToken = request.headers.get("Authorization")
        if not authToken or not authToken.startswith("Bearer"):
            return await call_next(request)
            
        accessToken = authToken.split(" ")[1]
    
        try:
            payload = verifyJwt(token=accessToken,keyIdentifier='ACCESSTOKENPUBLICKEY')
            if payload is not isinstance(ExpiredSignatureError,JWTError):
                request.state.user = payload
        except Exception:
            return await call_next(request)        
        return await call_next(request)      