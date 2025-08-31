# 全局默认的测试context 

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    # 假设 /auth/login 返回 token
    response = client.post("/auth/login", json={"username": "alice", "password": "secret"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
