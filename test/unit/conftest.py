# 仅unit test子文件夹生效的测试context
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.server import App                # 你定义的 App 类
from app.routes.user import Route as UserRoute
from app.controllers.user import UserController
from app.config.config import settings      # ✅ 从配置文件导入 settings


@pytest.fixture
def mock_user_controller():
    return AsyncMock(spec=UserController)


@pytest.fixture
def client(mock_user_controller):
    # 构建 user 路由
    user_route = UserRoute(mock_user_controller)

    # 用 App 类统一挂载路由 & 中间件
    application = App(routes=[user_route]).app

    return TestClient(application)
