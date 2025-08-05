from app.services import user, session
from app.model.user import UsersModel
from app.schemas.user import UserCreate, userLogin
from typing import Annotated
from fastapi import Form, Path, Query, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from motor.core import AgnosticDatabase
from app.config.debs import get_db
from odmantic import ObjectId, query
from app.utils.utilities import JsonRes, SignJwt
from app.model.session import SessionsModel
from app.schemas.session import SessionCreate
from app.config.config import settings
from app.utils.emails import SendEmail, EmailOptions
from fastapi.security import OAuth2PasswordRequestForm


class UserController:

    def __init__(self):
        self.UserService = user.UserService(UsersModel)
        self.sessionService = session.SessionService(SessionsModel)

    async def createUser(
        self,
        request: Request,
        id: Annotated[ObjectId | str, Path()],
        user: Annotated[UserCreate, Form()],
        db: AgnosticDatabase = Depends(get_db),
    ):
        adminUser = await self.UserService.GetUser(
            UsersModel.id == id and UsersModel.role == "admin"
        )

        # userInState = request.state.user
        # print(userInState['user']['id'])

        if not adminUser or "write" and "delete" not in adminUser.permissions:
            raise HTTPException(403, detail="there are no sufficient priviliages")

        existedUser = await self.UserService.GetUser(UsersModel.email == user.email)

        if existedUser:
            raise HTTPException(
                400, detail=f"user with email: {existedUser.email} already exists"
            )

        createdUser = await self.UserService.createUser(db, Input=user)

        if createdUser is None:
            raise HTTPException(400, detail="error creating the user")

        email_verification = SendEmail(
            EmailOptions(
                subject=settings.PROJECT_NAME + " Email verification",
                template_name="emailVerification.html",
                email_to=createdUser.email,
                link=settings.FRONTEND_MAIN_ORIGIN,
                to=createdUser.full_name,
            )
        )

        email_verification.execute()

        return JsonRes("user", createdUser, 201, "user created successfully")

    async def login(self, user: Annotated[OAuth2PasswordRequestForm , Depends()]):
        RESULT = await self.UserService.Authenticate(user.username, user.password)
        if not RESULT:
            raise HTTPException(403, detail="invalid credentials")

        existedUser = await self.UserService.GetUser(UsersModel.email == user.username)

        if not existedUser:
            raise HTTPException(404, detail="user not found")

        sessionObj = SessionCreate(userId=existedUser.id)

        await self.sessionService.createSession(sessionObj)

        userObj = {
            "id": str(existedUser.id),
            "email": existedUser.email,
            "full_name": existedUser.full_name,
        }

        accessToken = SignJwt(
            obj=userObj,
            expires_in=settings.ACCESS_TOKEN_EXPIRE,
            keyIdentifier="ACCESSTOKENPRIVATEKEY",
        )

        refreshToken = SignJwt(
            obj=userObj,
            expires_in=settings.REFRESH_TOKEN_EXPIRE,
            keyIdentifier="ACCESSTOKENPRIVATEKEY",
        )

        return JSONResponse(
            content={
                "message": "logged is successfully",
                "accessToken": accessToken,
                "refreshToken": refreshToken,
            },
            headers={
                "Authorization": f"Bearer {accessToken}",
                "x-refresh": refreshToken,
            },
        )

    async def getUser(
        self,
        id: Annotated[str | ObjectId, Path()],
        token:str
    ):

        user = await self.UserService.GetUser(query=UsersModel.id == id)
        print(token)
        if user is None:
            raise HTTPException(404, detail="user not found")

        return user

    async def getAllUsers(self, query: Annotated[str | None, Query()] = None):
        def errorUserNotFound(users: list[UsersModel] | None):
            if not users or len(users) < 1:
                raise HTTPException(
                    404, detail="there are not any users in the database  "
                )

        filters = {}
        if query:
            filters = {"full_name": {"$regex": f"^{query}", "$options": "i"}}

        users = await self.UserService.getAllUsers(query=filters if filters else None)

        errorUserNotFound(users)

        return users
