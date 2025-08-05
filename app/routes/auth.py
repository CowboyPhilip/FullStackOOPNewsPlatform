from typing_extensions import Annotated, Doc
from fastapi import APIRouter, Form, Depends,Header
from fastapi.param_functions import Form
from app.interfaces.main import Route as RouteInterface
from typing import Annotated
from app.schemas.user import userLogin
from app.controllers.user import UserController
from app.utils.utilities import oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm


class Login(OAuth2PasswordRequestForm):
    def __init__(
        self,
        *,
        email: str,
        password: str,
    ):
        super().__init__(
            username=email,
            password=password,
        )
        
       


class Route(RouteInterface):
    def __init__(self, userController: UserController):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.setup_routes()
        self.userController = userController

    def setup_routes(self):
        @self.router.post("/login", status_code=200 )
        async def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
            return await self.userController.login(user)
