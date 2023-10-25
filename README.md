# celery_django_docker
How to install celery and work with it using django and docker.

We will assume that you already have Django configured.

First, install celery ```pip install celery```

Then create ```celery.py``` file where the django ```settings.py``` is located.

Inside ```celery.py``` file paste 

```
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'path/to/django/settings.settings')

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def task(self):
    # some task
    pass
```

Hence, inside ```project/__init__.py``` (where ```settings.py``` file is located) paste this code

```
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

Then, inside app directory create file ```tasks.py``` and start writing your tasks:

```
from celery import shared_task
from django.conf import settings


@shared_task
def some_task():
    # do something
    pass
```

To send the tasks to celery-worker just use:
```
from . import tasks

tasks.some_task.delay()
```

Now we have our celery done, but we should connect a broker to celery. We will use redis as a broker. 
Type ```pip install redis``` to install redis.

Then write in ```settings.py``` 
```CELERY_BROKER_URL = 'redis://redis:6379'```

This is all with redis.

To configure a docker we should create two files name ```Dockerfile``` and ```docker-compose```.

Paste this codes to ```Dockerfile``` and ```docker-compose.yaml``` respectively

Dockerfile
```
FROM python:3.11-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .


CMD ["python3", "path_to/manage.py", "runserver", "0.0.0.0:8000"]
```

And

docker-compose.yaml
```
version: "3.9"

services:
  redis:
    image: redis
    restart: always

  webapp:
    restart: always
    build:
      context: ./
    ports:
      - "8000:8000"
    command: ["python3", "path_to/manage.py", "runserver", "0.0.0.0:8000"]

  worker:
    restart: always
    build:
      context: ./
    volumes:
      - ./path/to/media/folder:/app/path/to/media/folder
    command: ['celery', '--workdir=./project/dir', '-A', 'project', 'worker']
```

To run our containers we should run this command

```docker-compose up --build```

This will do all the job.
