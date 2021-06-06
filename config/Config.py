from pydantic import BaseSettings

class Config(BaseSettings):

    #DB PARAMS
    db_host: str ="localhost"
    db_port: int =5432
    db_name: str ="postgres"
    db_user: str ="postgres"
    db_pwd: str ="pass123" #os.environ["POSTGRES_PASSWORD"]

    db_url = f'postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'

    BASE_DIR: str ="data/fashion-small/"
    images_dir = f"{BASE_DIR}/images"

    csv_file = f"{BASE_DIR}/styles.csv"

   