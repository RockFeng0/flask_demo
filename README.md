
# To start

This is a project template for [flask-restful](https://github.com/flask-restful/flask-restful) with blueprint

```bash
# 1. install dependencies
pip install -r requirements.txt

# 2. for windows, you need install below version 
# pip install redis==2.10.6
# pip install celery==3.1.25 

# 3. set environment 
c:\flask_demo>set FLASK_APP=manager.py

# 4.init database
c:\flask_demo>flask db init -d migrations_test
c:\flask_demo>flask db migrate -d migrations_test
c:\flask_demo>flask db upgrade -d migrations_test

# 5. start redis service with redis.windows.conf which is setted 'requirepass 123456'
C:\Redis-x64-3.0.504>redis-server redis.windows.conf

# 6. start celery service
c:\flask_demo>celery -A app.celery_demo worker --loglevel info -c 1 -P eventlet

# 7. for devlopment, serve with hot reload at localhost:5000
c:\flask_demo>flask run --port 5000 --debug

# 8. for production, linux, run the command
# flask serve

```

# Folder structure
* app - your back-end app of flask
    * com - your app common file 
    * src - source code
        * models - sqlalchemy models
        * resources - your restful api resources
        * routes
    * utils        
        * wsgi_server - gunicorn
    * config.py - your app configurations
    * views.py
* job - celery work
    * celery_tasks -your app celery tasks
    * schedule_funcs -your app apschedule jobs
    * config.py - your job configurations
* manager.py

# Demo API
> RestFul API
```
* GET /api/v1.0/organization/department?page=1&size=10
* POST /api/v1.0/organization/department
    * json data: {"name": "财务部", "desc": "xx"}
* GET /api/v1.0/organization/department/1
* PUT /api/v1.0/organization/department/1 
    * json data: {"name": "xx", "desc": "xx"}
* DELETE /api/v1.0/organization/department/1  

* GET /api/v1.0/organization/staff?page=1&size=10
* POST /api/v1.0/organization/staff
    * json data: {"name": "小红", "age": 18, "dep_id": 1}
* GET /api/v1.0/organization/staff/1
* PUT /api/v1.0/organization/staff/1 
    * json data: {"name": "xx", "age": 20}
* DELETE /api/v1.0/organization/staff/1  
```

> Celery Workers API
```
* GET /task/run?seconds=30
    * will return task id
* GET /task/running_status/<tid>
* GET /task/deactivate/<tid>
```

> Schedule Job API， See doc in [APSchedule](https://apscheduler.readthedocs.io/en/latest/userguide.html#basic-concepts)
```
* GET /scheduler/jobs
* POST /scheduler/jobs
    * json data: 
    {
        "id": "schedule_task_1", 
        "func": "app.celery_demo.services.schedule_demo_task:add_task",  
        "args": [3, 4], 
        "kwargs": {},
        "trigger": "date",
        "run_date": "2021-01-05 23:05"
    }

* GET /scheduler/jobs/<job_id>
* PATCH /scheduler/jobs/<job_id>
    * json data, please see POST /scheduler/jobs, for example(each 5 seconds to run,):
         {"trigger": "cron", "second": "*/5"}
* DELETE /scheduler/jobs/<job_id>
    
* POST /scheduler/jobs/<job_id>/pause
    * json data: {}
* POST /scheduler/jobs/<job_id>/run
    * json data: {}
* POST /scheduler/jobs/<job_id>/resume
    * json data: {}
 
```

> User Auth
```
* POST /user/register
    * 用户注册,邮箱和手机号码是唯一的
    * {"email": "test@1234.com", "mobile_number": "13512341234", "username": "test", "password": "123456", "about_me": "测试注册功能"}
* POST /user/login
    * 邮箱或手机号登录
    * {"email_or_mobile_number": "test","password": "123456", "remember": false}
* POST /user/updater/1
    * 用户信息修改, 邮箱和手机号码是唯一的, 密码不能修改
    * {"email": "test@1234.com", "mobile_number": "13512341234", "username": "test", "about_me": "测试注册功能"}
    * {"mobile_number": "13512345678", "username": "test", "about_me": "测试注册功能"}
* GET /user/test
    * 鉴权测试
* GET /user/logout
```


# License
[MIT](http://opensource.org/licenses/MIT)
