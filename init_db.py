"""initialize database

create tables with given details

uses sqlalchemy create engine and sessionmaker 

requires config.Config module for database connection string

"""

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.Config import Config

config = Config()

metadata = MetaData(schema="public")

style = Table('style', metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('gender', String(50)),
    Column('masterCategory', String(100)),
    Column('subCategory', String(100)),
    Column('articleType', String(100)),
    Column('baseColour', String(100)),
    Column('season', String(100)),
    Column('year', Integer),
    Column('usage', String(100)),
    Column('productDisplayName', String(300)),
    Column('file_url', String(250))
)

engine = create_engine(config.db_url)
session = sessionmaker(bind=engine)()

metadata.create_all(bind=engine)