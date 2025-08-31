import pytest

def test_index_status(client):
    """测试首页是否能正常访问"""
    resp = client.get("/")
    assert resp.status_code == 200


def test_index_content_type(client):
    """测试返回类型是否正确 (HTML 或 JSON)"""
    ct = client.get("/").headers["content-type"]
    assert ct.startswith("text/html") or ct.startswith("application/json")


def test_index_contains_keyword(client):
    """测试返回内容是否包含欢迎信息或关键字"""
    resp = client.get("/")
    body = resp.text.lower()
    assert "welcome" in body or "news" in body or "ok" in body


def test_index_wrong_method(client):
    """测试首页禁止不正确的 HTTP 方法"""
    resp = client.post("/")  # 假设首页只允许 GET
    assert resp.status_code in (405, 404)


def test_notfound_route(client):
    """测试不存在的路由返回 404"""
    resp = client.get("/nonexistent-path")
    assert resp.status_code == 404
