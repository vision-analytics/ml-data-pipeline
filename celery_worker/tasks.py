""" Task definitions for Celery
You can add new tasks like following one:

@app.task
def add(x, y):
    return x + y

"""

import logging
import os

import celery
from celery import Celery
from celery.schedules import crontab

import app as mldp_app

app = Celery(
    'tasks',
    broker=os.environ.get('CELERY_BROKER', "redis://localhost:6379/0"), 
    backend=os.environ.get('CELERY_BACKEND', "redis://localhost:6379/0")
    )


@celery.signals.setup_logging.connect  
def setup_celery_logging(**kwargs):  
    return logging.getLogger('celery')

@app.task
def add(x, y):
    return x + y

@app.task
def sample_run():
    mldp_app.run()
    