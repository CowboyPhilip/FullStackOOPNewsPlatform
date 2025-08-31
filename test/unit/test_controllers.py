import pytest
from unittest.mock import AsyncMock
from app.controllers.user_controller import UserController

@pytest.mark.asyncio
async def test_get_user_controller():
    # mock model 层
    mock_model = AsyncMock()
    mock_model.get_user.return_value = {"id": "1", "name": "Charlie"}

    controller = UserController(user_model=mock_model)
    result = await controller.getUser("1", "token123")

    assert result == {"id": "1", "name": "Charlie"}
    mock_model.get_user.assert_awaited_once_with("1")
