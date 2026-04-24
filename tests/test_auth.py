#! python3
# -*- encoding: utf-8 -*-

import json


def test_register(client):
    """测试用户注册"""
    response = client.post(
        "/user/register",
        data=json.dumps({
            "email": "test@example.com",
            "mobile_number": "13800138000",
            "username": "testuser",
            "password": "password123"
        }),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["code"] == 200


def test_login(client):
    """测试用户登录"""
    # 先注册用户
    client.post(
        "/user/register",
        data=json.dumps({
            "email": "test@example.com",
            "mobile_number": "13800138000",
            "username": "testuser",
            "password": "password123"
        }),
        content_type="application/json"
    )
    
    # 测试登录
    response = client.post(
        "/user/login",
        data=json.dumps({
            "email_or_mobile_number": "test@example.com",
            "password": "password123"
        }),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["code"] == 200
    assert "token" in data["data"]


def test_logout(client):
    """测试用户注销"""
    # 先注册用户
    client.post(
        "/user/register",
        data=json.dumps({
            "email": "test@example.com",
            "mobile_number": "13800138000",
            "username": "testuser",
            "password": "password123"
        }),
        content_type="application/json"
    )
    
    # 登录获取token
    login_response = client.post(
        "/user/login",
        data=json.dumps({
            "email_or_mobile_number": "test@example.com",
            "password": "password123"
        }),
        content_type="application/json"
    )
    token = json.loads(login_response.data)["data"]["token"]
    
    # 测试注销
    response = client.get(
        "/user/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["code"] == 200