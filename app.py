import json
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from sqlalchemy import and_

from api import query
from config.Config import Config
from models.Style import Style
from utils.ImageAugmentation import ImageAugmentation
from utils.ModelInference import ModelInference
from utils.S3Handler import S3Handler


config = Config()

def run_new_query():
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
        
        if obj.key.endswith('.json'): #read json files only
            print(obj.key)
            file_body = obj.get()['Body'].read()
            data = json.loads(file_body)
            dfs.append(pd.json_normalize(data))
            
    df = pd.concat(dfs, sort=False)
    print("!! DONE | READING QUERY RESULTS FROM s3 !!")
    del s3_handler
    return df
        
def run_augmentations(df=None, n_of_samples=10):
    print("!! RUNNING IMAGE AUGMENTATION !!")

    s3_handler = S3Handler()
    img_aug = ImageAugmentation()
    
    #create directory for augmented images if not exists
    if not os.path.exists(config.augmented_images_dir):
        os.makedirs(config.augmented_images_dir)

    for index, row in df.sample(n = n_of_samples).iterrows():
        print( row['id'], row['s3_url'])

        image = s3_handler.read_image_from_s3(row['s3_url'])
        
        transformed_img = img_aug.random_resized_crop(
            image=image,
            width=256, 
            height=256, 
            scale=(0.8, 0.8)
            )
        
        #writing augmented images to new directory. #TODO: 
        aug_file_path = "{}_aug.jpg".format(os.path.splitext(row['s3_url'])[0]) #row['s3_url'].split('/')[-1]
        local_file_path = "{}_aug.jpg".format(os.path.splitext(row['local_url'].split('/')[-1])[0])

        transformed_img_path = os.path.join(config.augmented_images_dir, local_file_path)

        #display image
        #plt.imshow(transformed_img)
        #plt.show()

        #write image to file
        im = Image.fromarray(transformed_img)
        im.save(transformed_img_path)
        s3_handler.upload_file(transformed_img_path, aug_file_path)
    
    del s3_handler
    print(f"!! DONE | IMAGE AUGMENTATION | AUGMENTED IMAGES BOTH UPLOADED TO S3 AND EXPORTED TO: {config.augmented_images_dir}!!")
        
def run_model_inference(df=None, n_of_samples=10):
    print("!! RUNNING MODEL INFERENCE !!")

    def rows_to_json_and_s3(x):
        """function to write df rows to both local and s3 bucket"""
        x.to_json(f"{config.augmented_images_dir}/{x.id}_v2.json")

        #upload to s3
        s3_obj_key = os.path.splitext(x.s3_url)[0] + '_v2.json'
        s3_handler.write_json_to_s3_file(x.to_json(), s3_obj_key)


    #run inference on 10 images and update jsons
    s3_handler = S3Handler()

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
        #print(index, row['id'], row['s3_url'])
        #image_path = os.path.join(os.environ["PYTHONPATH"], row['local_url'])
        image = s3_handler.read_image_from_s3(row['s3_url'])
        
        #plt.imshow(plt.imread(image_path))
        #plt.show()
        out = model.predict(image)
        print("model inference results : ", row['id'], out)
        
        df.loc[df.id == row['id'], 'fashionnet_category_name'] = out.get('category_name','')
        df.loc[df.id == row['id'], 'fashionnet_category_type'] = out.get('category_type','')
        df.loc[df.id == row['id'], 'fashionnet_attribute_name'] = out.get('attribute_name','')
        df.loc[df.id == row['id'], 'fashionnet_attribute_type'] = out.get('attribute_type','')
        
    #write each row to new seperate json files
    df.apply(rows_to_json_and_s3, axis=1)

   
    print(f"!! DONE | MODEL INFERENCE | JSON FILES WITH NEW VALUES BOTH UPLOADED TO S3 AND EXPORTED TO: {config.augmented_images_dir}!!")
    del model, s3_handler



def run():
    #run query
    run_id = run_new_query()
    
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