from app.config.config import settings


def test_create_user(client, mock_user_controller):
    mock_user_controller.createUser.return_value = {"id": "2", "name": "Alice"}

    url = f"{settings.API_V1_STR}/users"  # ✅ 从 settings 引用
    response = client.post(url, json={"name": "Alice"}, headers={"Authorization": "Bearer faketoken"})

    assert response.status_code == 200
    assert response.json() == {"id": "2", "name": "Alice"}
    
def test_get_user(client, mock_user_controller):
    mock_user_controller.getUser.return_value = {"id": "1", "name": "Bob"}

    url = f"{settings.API_V1_STR}/users/1"  # ✅ 从 settings 引用
    response = client.get(url, headers={"Authorization": "Bearer faketoken"})

    assert response.status_code == 200
    assert response.json() == {"id": "1", "name": "Bob"}


def test_get_users(client, mock_user_controller):
    mock_user_controller.getUsers.return_value = [
        {"id": "1", "name": "Bob"},
        {"id": "2", "name": "Alice"}
    ]

    url = f"{settings.API_V1_STR}/users"  # ✅ 从 settings 引用
    response = client.get(url, headers={"Authorization": "Bearer faketoken"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": "1", "name": "Bob"},
        {"id": "2", "name": "Alice"}
    ]