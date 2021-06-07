""" init module for submitting new ASYNC task to Celery

requires celery_worker.tasks module

"""

import sys
import os
from celery_worker import tasks

if __name__ == "__main__":
    tasks.sample_run.apply_async(args=[]) 