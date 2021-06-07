import os
import pandas as pd
from pydantic import BaseSettings
from pydantic.tools import T

class Config(BaseSettings):

    app_root: str = "/app"
    working_dir: str = "/pv"

    #DB PARAMS
    db_host: str = "postgres" #localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_pwd: str = os.environ["POSTGRES_PASSWORD"]

    db_url = f'postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

    BASE_DIR: str = f"{working_dir}/data/fashion-small/"
    images_dir = f"{BASE_DIR}/images"

    csv_file = f"{BASE_DIR}/styles.csv"
    augmented_images_dir = f"{working_dir}/augmented"

    #AWS
    AWS_ACCESS_KEY_ID: str = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY: str = os.environ["AWS_SECRET_ACCESS_KEY"]
    AWS_REGION_NAME: str = "eu-west-1"
    AWS_BUCKET_NAME: str = os.environ["AWS_BUCKET_NAME"]
    AWS_OUT_DIR: str = "query_results"

    #CELERY
    CELERY_BROKER: str = "redis://localhost:6379/0"
    CELERY_BACKEND: str = "redis://localhost:6379/0"
   
