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
        # 处理该请求时 框架会尝试解析request，id，user三个参数
        # request是特殊参数 HTTP请求本身 包含request line, headers, body  已经在starlette的context里
        # 其他普通参数根据最高优先级的type hint推断，id和user分别从path和form data里提取

        # Annotated[str | ObjectId, Path()]中
        # Path类的作用： 1. 声明该参数从HTTP path里提取 2. 可以添加额外的元数据 例如description, example， 验证逻辑 max_length, min_length, regex
        # Annotated的作用： 把参数来源（type hints）和参数内容(str | ObjectId) 绑定 可以添加多个type hint （Query()、Path()、Body()、Form()） 
        @self.router.post("/{id}", status_code=201)
        async def CreateUser(
            request:Request,id: Annotated[str | ObjectId, Path()], user: Annotated[UserCreate, Form()]
        ):
            # 只接收 把解析到的id和user传给controller 在controller里才进行业务逻辑处理 并调用model层持久化
            return await self.userController.createUser(request,id,user)

        @self.router.get("/{id}", response_model=User)
        async def getUser(id: Annotated[str, ObjectId, Path()] ,token:Annotated[str,Depends(oauth2_scheme)] ):
            return await self.userController.getUser(id,token)

        @self.router.get("/", response_model=list[User])
        async def getAllUsers(name: Annotated[str | None, Query()] = None):
            if name is not None:
                return await self.userController.getAllUsers(query=name)
            return await self.userController.getAllUsers()
