from pydantic import BaseSettings

class Config(BaseSettings):

    working_dir = "pv"

    #DB PARAMS
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str = "postgres"
    db_pwd: str = "pass123" #os.environ["POSTGRES_PASSWORD"]

    db_url = f'postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

    BASE_DIR: str = "data/fashion-small/"
    images_dir = f"{BASE_DIR}/images"

    csv_file = f"{BASE_DIR}/styles.csv"

    #AWS
    AWS_ACCESS_KEY_ID: str = "AKIAVODZ5ZX3YR2RZUF4"
    AWS_SECRET_ACCESS_KEY: str = "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"
    AWS_REGION_NAME: str = "eu-west-1"
    AWS_BUCKET_NAME: str = "mldp-06062021"
    AWS_OUT_DIR: str = "query_results"
   