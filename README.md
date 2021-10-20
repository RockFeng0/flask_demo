
# To start

This is a project template for [flask-restful](https://github.com/flask-restful/flask-restful) with blueprint

```bash
# install dependencies
pip install -r requirements.txt

# for windows, you need install below version 
# pip install redis==2.10.6
# pip install celery==3.1.25 

# init database
python3 manager.py db init
python3 manager.py db migrate
python3 manager.py db upgrade

# start redis service with redis.windows.conf which is setted 'requirepass 123456'
C:\Redis-x64-3.0.504>redis-server redis.windows.conf

# start celery service
cd c:\flask_demo>celery worker -A job --loglevel info -c 1

# for devlopment, serve with hot reload at localhost:5000
python3 manager.py debug

# for production
python3 manager.py run

```

# Folder structure
* app - your back-end app of flask
    * models - sqlalchemy models
    * resources - your restful api resources
    * views - your blueprints and apis    
    * config.py - your flask app configurations
    * code.py - http response code
    * pretty.py
* job - asynchronous tasks and schedule tasks  (celery + redis + aspschedule)
    * celery_tasks -your app celery tasks
    * schedule_funcs -your app apschedule jobs
    * config.py - your job configurations
* utils - utils or extensions
    * email - to do
    * wsgi_server - gunnicorn command line
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
        "func": "job.schedule_funcs.demo_func:add_task", 
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
 



# License
[MIT](http://opensource.org/licenses/MIT)
