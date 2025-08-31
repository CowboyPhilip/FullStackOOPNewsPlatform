from app.routes import index,users,blog
from app.interfaces.main import Route
from app.controllers.user import UserController

# 初始化route list （路由表） 包含三个路由 路径分别为xxx.com/index, xxx.com/users, xxx.com/blog
# route应该有以下field: 
# 和以下method:
routes:list[Route] = [
    index.Route(),
    users.Route(UserController()),
    blog.Route()
]