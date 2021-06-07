"""TODO: update docs

"""
import os

import pandas as pd
from sqlalchemy import create_engine

from config.Config import Config

def _file_url_generator(base_path, row):
    return '{}/{}.jpg'.format(base_path,row['id'])

config = Config()

#read csv
all_metadata = pd.read_csv(config.csv_file, usecols=['id', 'gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'year', 'usage', 'productDisplayName'])

#drop rows which contain null(nan) values
all_metadata = all_metadata.dropna()

# add file urls to df. (images.csv not found in fashion-small dataset)
all_metadata['file_url'] = all_metadata.apply (lambda row: _file_url_generator(config.images_dir, row), axis=1)

engine = create_engine(config.db_url)

#uncomment following line to increase data size x30
#all_metadata = pd.concat([all_metadata]*30, ignore_index=True) 

#export data to postgres
all_metadata.to_sql('style', engine, index=False, if_exists='replace')