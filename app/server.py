from abc import ABC
from fastapi import FastAPI
from app.interfaces.main import Route
from app.middlewares.serializeUser import Auth
from app.config.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.routes import auth
from app.controllers.user import UserController

class App(ABC):
    app: FastAPI

    # 一个fastapi app实例最重要的功能：实现routes和middlewares
    # route 例子: xxx.com/api/v1/auth/login
    # middleware 例子: xxx.com/api/v1/auth/login -> Auth Middleware -> Auth Controller 在这个过程中 对于所有经过该route的请求 进行统一处理 例如logger，鉴权
    # （route/middlewares）写在另外的类里 这个方法叫模块化 目的是更好地解耦 具体表现是减少main entry的代码量 + 便于复用和修改
    def __init__(self, routes: list[Route]):
        self.app = FastAPI(title=settings.PROJECT_NAME)
        self.app.include_router(auth.Route(UserController()).router)
        self.initializeRoutes(routes)
        self.initializeBuiltMiddlewares()
        self.initializeMiddlewares()

    def initializeRoutes(self, routes: list[Route]):
        # Example usage of routes
        for route in routes:
            self.app.include_router(route.router, prefix=settings.API_V1_STR)

    def initializeBuiltMiddlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def initializeMiddlewares(self):
        self.app.add_middleware(Auth)
