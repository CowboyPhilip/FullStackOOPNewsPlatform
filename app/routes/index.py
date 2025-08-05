from fastapi import APIRouter
from app.interfaces.main import Route as RouteInterface
class Route(RouteInterface):
    def __init__(self):
        self.router = APIRouter(prefix="", tags=["index"])
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/")
        async def checkServer():
            return {"message": "server is responding on port {}"}
