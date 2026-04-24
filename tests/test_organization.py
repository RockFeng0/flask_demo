#! python3
# -*- encoding: utf-8 -*-

import json


def test_department_creation(client):
    """测试部门创建"""
    response = client.post(
        "/organization/department",
        data=json.dumps({
            "name": "测试部门",
            "desc": "这是一个测试部门"
        }),
        content_type="application/json"
    )
    data = json.loads(response.data)
    print(data)
    assert response.status_code == 200

    assert data["code"] == 200


def test_department_list(client):
    """测试获取部门列表"""
    # 先创建一个部门
    client.post(
        "/organization/department",
        data=json.dumps({
            "name": "测试部门",
            "desc": "这是一个测试部门"
        }),
        content_type="application/json"
    )
    
    # 测试获取部门列表
    response = client.get("/organization/department")
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data)
    assert data["code"] == 200
    assert "departments" in data["data"]


def test_staff_creation(client):
    """测试职工创建"""
    # 先创建一个部门
    client.post(
        "/organization/department",
        data=json.dumps({
            "name": "测试部门",
            "desc": "这是一个测试部门"
        }),
        content_type="application/json"
    )
    
    # 测试创建职工
    response = client.post(
        "/organization/staff",
        data=json.dumps({
            "name": "测试职工",
            "age": 25,
            "dep_id": 1
        }),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data)
    assert data["code"] == 200


def test_staff_list(client):
    """测试获取职工列表"""
    # 先创建一个部门
    client.post(
        "/organization/department",
        data=json.dumps({
            "name": "测试部门",
            "desc": "这是一个测试部门"
        }),
        content_type="application/json"
    )
    
    # 再创建一个职工
    client.post(
        "/organization/staff",
        data=json.dumps({
            "name": "测试职工",
            "age": 25,
            "dep_id": 1
        }),
        content_type="application/json"
    )
    
    # 测试获取职工列表
    response = client.get("/organization/staff")
    assert response.status_code == 200
    data = json.loads(response.data)
    print(data)
    assert data["code"] == 200
    assert "staffs" in data["data"]