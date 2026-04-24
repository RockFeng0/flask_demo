# Flask Demo

这是一个基于 Flask 的 RESTful API 项目模板，集成了 Flask-RESTful、SQLAlchemy、Celery 等常用扩展。

## 功能特性

- RESTful API 设计
- SQLAlchemy ORM 数据库操作
- Celery 异步任务处理
- Flask-Login 用户认证
- Redis 缓存支持
- 环境变量配置管理
- 完整的测试用例

## 技术栈

- **Web 框架**: Flask, Flask-RESTful
- **数据库**: SQLAlchemy, Flask-Migrate
- **任务队列**: Celery, Redis
- **认证**: Flask-Login, Flask-Bcrypt
- **缓存**: Flask-Caching, Redis
- **依赖管理**: uv

## 快速开始

### 1. 安装依赖

```bash
# 使用 uv 安装依赖
uv sync
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并根据实际情况修改配置：

```bash
cp .env.example .env
```

### 3. 初始化数据库

```bash
# 创建迁移目录
flask db init -d migrations

# 生成迁移脚本
flask db migrate -d migrations

# 执行迁移
flask db upgrade -d migrations
```

### 4. 启动 Redis 服务

确保 Redis 服务正在运行，默认配置：

- 端口：6379
- 123456
- 
```bash
D:\Redis-x64-3.0.504>redis-server.exe redis.windows.conf
```


### 5. 启动 Celery Worker

```bash
d:\flask_demo>celery -A app.tasks.celery worker --loglevel info -c 1 -P eventlet
```

### 6. 启动开发服务器

```bash
# 开发模式（热重载）
d:\flask_demo>flask run --port 5000 --debug

# 或使用命令
flask serve
```

### 7. 运行测试

```bash
d:\flask_demo>uv run pytest tests/ -v
```

## 项目结构

```
flask_demo/
├── app/
│   ├── blueprints/          # 蓝图模块
│   │   ├── auth/           # 用户认证模块
│   │   ├── celery/         # Celery 任务管理模块
│   │   └── organization/   # 组织管理模块
│   ├── common/             # 通用工具
│   │   ├── code.py        # 错误码定义
│   │   └── response/       # 响应格式化
│   ├── config/             # 配置模块
│   │   ├── base.py        # 基础配置
│   │   ├── dev.py         # 开发环境配置
│   │   └── prod.py        # 生产环境配置
│   ├── models/             # 数据模型
│   │   ├── user.py        # 用户模型
│   │   ├── department.py  # 部门模型
│   │   └── staff.py       # 员工模型
│   ├── tasks/             # Celery 任务
│   │   └── celery/        # Celery 任务定义
│   └── utils/             # 工具函数
│       ├── email/         # 邮件工具
│       └── wsgi_server/   # WSGI 服务器配置
├── tests/                  # 测试用例
├── migrations/            # 数据库迁移
├── logs/                  # 日志文件
├── manager.py             # 应用入口
└── pyproject.toml         # 项目配置
```

## API 接口

### 用户认证

```
# 用户注册
POST /user/register
{
    "email": "test@example.com",
    "mobile_number": "13800138000",
    "username": "test",
    "password": "123456"
}

# 用户登录
POST /user/login
{
    "email_or_mobile_number": "test@example.com",
    "password": "123456"
}

# 用户登出
GET /user/logout
```

### 组织管理

```
# 部门管理
GET /organization/department?page=1&size=10
POST /organization/department
    {"name": "财务部", "desc": "财务管理部门"}
GET /organization/department/<id>
PUT /organization/department/<id>
    {"name": "人力资源部", "desc": "人力资源管理部门"}
DELETE /organization/department/<id>

# 员工管理
GET /organization/staff?page=1&size=10
POST /organization/staff
    {"name": "张三", "age": 28, "dep_id": 1}
GET /organization/staff/<id>
PUT /organization/staff/<id>
    {"name": "李四", "age": 30}
DELETE /organization/staff/<id>
```

### Celery 任务

```
# 运行普通任务
GET /task/run?seconds=10

# 运行高优先级任务
POST /task/run_high_priority
    {"data": "high priority task"}

# 运行低优先级任务
POST /task/run_low_priority
    {"data": "low priority task"}

# 获取任务状态
GET /task/status/<task_id>

# 取消任务
POST /task/cancel/<task_id>

# 获取 Worker 状态
GET /task/workers

# 获取队列状态
GET /task/queues

# 获取统计信息
GET /task/stats
```

### 定时任务

```
# 获取所有定时任务
GET /scheduler/jobs

# 添加定时任务
POST /scheduler/jobs
{
    "id": "schedule_task_1",
    "func": "app.tasks.celery.schedule_demo_task:add_task",
    "args": [3, 4],
    "trigger": "date",
    "run_date": "2024-01-05 23:05"
}

# 暂停定时任务
POST /scheduler/jobs/<job_id>/pause

# 恢复定时任务
POST /scheduler/jobs/<job_id>/resume

# 删除定时任务
DELETE /scheduler/jobs/<job_id>
```

## 配置说明

### 环境变量

```bash
# 应用环境
APP_ENV=development  # development, production, testing

# Flask 配置
SECRET_KEY=your-secret-key
FLASK_APP=manager.py

# 数据库配置
DATABASE_URL=sqlite:///flask_demo.db

# Redis 配置
REDIS_URL=redis://127.0.0.1:6379/0

# Celery 配置
CELERY_BROKER_URL=redis://127.0.0.1:6379
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
```

## 开发指南

### 添加新的蓝图模块

1. 在 `app/blueprints/` 目录下创建新的蓝图文件夹
2. 创建 `routes.py` 文件，定义路由和视图函数
3. 在 `app/__init__.py` 中注册蓝图

### 添加新的数据模型

1. 在 `app/models/` 目录下创建新的模型文件
2. 继承 `app.models.base.BaseModel` 基类
3. 定义字段和关系

### 添加新的 Celery 任务

1. 在 `app/tasks/celery/` 目录下创建新的任务文件
2. 使用 `@celery.task` 装饰器定义任务
3. 更新 `app/tasks/celery/conf.py` 中的任务导入配置

## 生产部署

### 使用 Gunicorn

```bash
flask serve
```

### 使用 Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "manager:APP"]
```

## License

[MIT](http://opensource.org/licenses/MIT)