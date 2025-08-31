from fastapi import APIRouter
from app.interfaces.main import Route as RouteInterface

# 根路由 网页的初始页面 返回网页是否在正常运行
# Route类是@app.get()等注解的底层实现 （继承自fastapi.APIRoute）  
# 但这里我们自定义的Route类 继承自RouteInterface(一个本项目自定义的route接口，实现可以替换为别的， 例如fastapi.APIRouter 例如typing.Protocol)

class Route(RouteInterface):
    def __init__(self):
        self.router = APIRouter(prefix="", tags=["index"])
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/")
        async def checkServer():
            return {"message": "server is responding on port {}"}
