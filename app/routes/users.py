from app.interfaces.main import Route as RouteInterface
from typing import Annotated
from fastapi import Query, Path, Form, APIRouter,Request,Depends
from app.controllers.user import UserController
from app.schemas.user import UserCreate, User, userLogin
from odmantic import ObjectId
from app.utils.utilities import oauth2_scheme

class Route(RouteInterface):

    def __init__(self, userController: UserController):
        self.router = APIRouter(prefix="/users", tags=["users"])
        self.setup_routes()
        self.userController = userController

    def setup_routes(self):

        @self.router.post("/{id}", status_code=201)
        async def CreateUser(
            request:Request,id: Annotated[str | ObjectId, Path()], user: Annotated[UserCreate, Form()]
        ):
            return await self.userController.createUser(request,id,user)

        @self.router.get("/{id}", response_model=User)
        async def getUser(id: Annotated[str, ObjectId, Path()] ,token:Annotated[str,Depends(oauth2_scheme)] ):
            return await self.userController.getUser(id,token)

        @self.router.get("/", response_model=list[User])
        async def getAllUsers(name: Annotated[str | None, Query()] = None):
            if name is not None:
                return await self.userController.getAllUsers(query=name)
            return await self.userController.getAllUsers()
