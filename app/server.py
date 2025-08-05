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
