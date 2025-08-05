from app.routes import index,users,blog
from app.interfaces.main import Route
from app.controllers.user import UserController
routes:list[Route] = [
    index.Route(),
    users.Route(UserController()),
    blog.Route()
]