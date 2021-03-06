import json
import os
import time
import tqdm
import uuid

from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker

from config.Config import Config
from models.Style import Style
from utils.S3Handler import S3Handler

config = Config()

db = create_engine(config.db_url)

Session = sessionmaker(db)  
session = Session()

s3_handler = S3Handler()

def generate_uuid():
    """ Generate uuid for each query"""
    return str(uuid.uuid4())

def export_to_s3(exp_id, data):
    """Export data to s3 for given experiment id

    Parameters
    ----------
    exp_id : str
        generated uuid
    data : obj, 
        result of query

    Returns
    -------
    
    """
    out_dir = os.path.join(config.AWS_OUT_DIR, exp_id) # folder to keep files in s3

    # write to json
    for item in tqdm.tqdm(data):

        s3_obj_key_img = f"{out_dir}/{item.id}.jpg"
        s3_obj_key_json = f"{out_dir}/{item.id}.json"

        #upload image to s3
        s3_full_url = s3_handler.upload_file(item.file_url, s3_obj_key_img)

        #prepare json
        json_data = {    
            'id': item.id,
            'gender': item.gender,
            'masterCategory': item.masterCategory,
            'subCategory': item.subCategory,
            'articleType': item.articleType,
            'baseColour': item.baseColour,
            'season': item.season,
            'year': item.year,
            'usage': item.usage,
            'productDisplayName': item.productDisplayName,
            'local_url': item.file_url,
            's3_url': s3_obj_key_img,
            's3_full_url': s3_full_url
            }
        
        #write json to s3 file
        s3_handler.write_json_to_s3_file(json_data, s3_obj_key_json)

def run_query(query_obj=None, filters=None, limit=None, upload_to_s3=False):
    """Gets and prints the spreadsheet's header columns

    Parameters
    ----------
    query_obj : obj
        Query object of sqlalchemy
    filters : obj
        combined filters (Filter object of sqlalchemy)
    limit : int
        result row limit. 
    upload_to_s3 : bool, optional
        A flag used to upload data to s3 (default is False)

    Returns
    -------
    run_id, 
        generated run_id for each run
    items,
        results
    """
    # query
    start_time = time.time()
    run_id = generate_uuid()
    print(f"run_id: {run_id}")

    print("running query")
    query_start_time = time.time()
    items = session.query(query_obj).filter(*filters).limit(limit)
    query_time = time.time() - query_start_time
    
    print(f"items count: {items.count()} | query took {query_time} seconds")
    if upload_to_s3: # not upload to s3 if testing
        s3_upload_start_time = time.time()
        print(f"uploading {items.count()} items to s3")
        export_to_s3(run_id, items)
        s3_upload_time = time.time() - s3_upload_start_time
        print(f"uploaded all items! | it took {s3_upload_time} seconds")

    time_elapsed = time.time() - start_time
    print(f"DONE! {run_id} | it took {time_elapsed} seconds")
    return run_id, items


def sample_query_1():
    #all types of male shoes years after 2012
    
    filters = [Style.gender == "Men", Style.subCategory == "Shoes", Style.year >= 2012]

    # query
    run_query(Style, filters, upload_to_s3=True)


def sample_query_2():
    #all types of woman bags for summer season

    filters = [Style.gender == "Women", Style.subCategory == "Bags", Style.season == "Summer"]

    # query
    run_query(Style, filters, upload_to_s3=True)


def sample_query_3():
    #all types of unisex watches before 2013
    
    filters = [Style.gender == "Unisex", Style.articleType == "Watches", Style.year >= 2013]

    # query
    run_query(Style, filters, upload_to_s3=True)




if __name__ == "__main__":
    sample_query_3()

    