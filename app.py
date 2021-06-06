import json
import os

import cv2
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import and_

from api import query
from config.Config import Config
from models.Style import Style
from utils.ImageAugmentation import ImageAugmentation
from utils.ModelInference import ModelInference
from utils.S3Handler import S3Handler


config = Config()

def run_query():
    print("!! RUNNING QUERY AND UPLOADING RESULTS TO s3 !!")
    # select filters
    filters=[Style.gender == "Unisex",
            #Style.articleType == "Watches",
            Style.year >= 2013]
    # run query
    run_id, items = query.run_query(Style, filters, limit=10, upload_to_s3=True)
    print("!! DONE | RUNNING QUERY AND UPLOADING RESULTS TO s3 !!")
    return run_id


def read_query_results(run_id):
    print("!! READING QUERY RESULTS FROM s3 !!")
    s3_handler = S3Handler()

    #TODO: update run_id!
    results = s3_handler.list_dir(run_id)

    #read data from s3 to pandas dataframe
    dfs = []

    for obj in results:
        print(obj.key)
        file_body = obj.get()['Body'].read()
        data = json.loads(file_body)
        dfs.append(pd.json_normalize(data))
        
    df = pd.concat(dfs, sort=False)
    print("!! DONE | READING QUERY RESULTS FROM s3 !!")
    return df
        
def run_augmentations(df=None, n_of_samples=10):
    print("!! RUNNING IMAGE AUGMENTATION !!")
    img_aug = ImageAugmentation()
    
    #create directory for augmented images if not exists
    if not os.path.exists(config.augmented_images_dir):
        os.makedirs(config.augmented_images_dir)

    for index, row in df.sample(n = n_of_samples).iterrows():
        print( row['id'])
        image_path = os.path.join(os.environ["PYTHONPATH"], row['file_url'])

        transformed_img = img_aug.random_resized_crop(
            image_path=image_path,
            width=256, 
            height=256, 
            scale=(0.8, 0.8)
            )
        
        #writing augmented images to new directory. #TODO: 
        transformed_img_path = os.path.join(config.augmented_images_dir, row['file_url'].split('/')[-1])
        
        #display image
        plt.imshow(transformed_img)
        plt.show()

        #write image to file
        cv2.imwrite(transformed_img_path, transformed_img[:,:,::-1]) #rgb to bgr
    print("!! DONE | IMAGE AUGMENTATION | AUGMENTED IMAGED WRITTEN TO: {config.augmented_images_dir}!!")
        
def run_model_inference(df=None, n_of_samples=10):
    print("!! RUNNING MODEL INFERENCE !!")

    #run inference on 10 images and update jsons

    #init model
    model = ModelInference()

    #create directory for augmented images if not exists
    if not os.path.exists(config.augmented_images_dir):
        os.makedirs(config.augmented_images_dir)

    #assign none to new columns 
    df['fashionnet_category_name'] = None
    df['fashionnet_category_type'] = None
    df['fashionnet_attribute_name'] = None
    df['fashionnet_attribute_type'] = None


    for index, row in df.sample(n = 10).iterrows():
        print(index, row['id'])
        image_path = os.path.join(os.environ["PYTHONPATH"], row['file_url'])
        plt.imshow(plt.imread(image_path))
        plt.show()
        out = model.predict(image_path)
        df.loc[df.id == row['id'], 'fashionnet_category_name'] = out['category_name']
        df.loc[df.id == row['id'], 'fashionnet_category_type'] = out['category_type']
        df.loc[df.id == row['id'], 'fashionnet_attribute_name'] = out['attribute_name']
        df.loc[df.id == row['id'], 'fashionnet_attribute_type'] = out['attribute_type']
    
        new_json_path = os.path.join(config.augmented_images_dir, row['file_url'].split('/')[-1]+'.json')

        #write data to new json
        row.to_json(new_json_path)
    print(f"!! DONE | MODEL INFERENCE | JSON FILES WITH NEW VALUES WRITTEN TO: {config.augmented_images_dir}!!")

def run():
    #run query
    run_id = run_query()
    
    #read query results
    df = read_query_results(run_id)

    #print(df.head(10))

    # to run experimental data analysis -> notebooks/run_query_and_perform_basic_data_analysis.ipynb

    # run augmentations and save output to directory
    run_augmentations(df=df, n_of_samples=10)

    # run model inference on sample set and write new json files to directory
    run_model_inference(df=df, n_of_samples=10)


if __name__ == '__main__':
    run()