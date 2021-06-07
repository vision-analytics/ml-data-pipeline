import sys
import os
from celery_worker import tasks

if __name__ == "__main__":
    tasks.sample_run.apply(args=[]) 