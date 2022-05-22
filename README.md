# Project Details
## ml-data-pipeline


```
project steps
- setup database (done!)

- load data from csv to database (after preprocessing) (done!)

- obtain subset of data with queries, generate json files and upload to s3 (seperate directories for each run) (done!)

- run exploratory data analysis (w. jupyter notebook) (done!)

- apply augmentations for subsets (done!)

- run pretrained model on subset and add new values to metadata(json) (done!)

- used celery for task management (ui: flower, broker: redis)

```


# &nbsp;

# Usage

```
# set environment variables in .env file

# start services
docker compose up

# open interactive shell(container) to run following commands
docker-compose exec celery_worker /bin/bash

# init db
-> python3 init_db.py

# export data from csv to db
-> python3 load_data_to_db.py

# submit sample task
-> python3 init_task.py

# check task status on ui -> http://localhost:5555/

#run jupyter notebooks (for both eda and )
jupyter notebook notebooks --allow-root --ip='*' --NotebookApp.token='' --NotebookApp.password=''
# -> open browser and go to -> http://localhost:8888/

# to run unit tests
-> pytest tests/unit_test.py


```


Custom queries can be added in api/query.py like following ones:
```
    def sample_query_1():
    #all types of male shoes years after 2012
    
    filters = [Style.gender == "Men", Style.subCategory == "Shoes", Style.year >= 2012]
    ...


    def sample_query_2():
    #all types of woman bags for summer season

    filters = [Style.gender == "Women", Style.subCategory == "Bags", Style.season == "Summer"]
    ...

    def sample_query_3():
    #all types of unisex watches before 2013
    
    filters = [Style.gender == "Unisex", Style.articleType == "Watches", Style.year >= 2013]
    ...
```

# &nbsp;

Structure:
```
.
+- api
|  - query.py - query operations and data upload
+- celery_worker
|  - tasks.py - celery task definitions
+- config
|  - Config.py - configuration module for keeping variables
|  - list_attr_cloth.txt - Classes for deepfashion model
|  - list_category_cloth.txt - Classes for deepfashion model
+- models
|  - Style.py - table structure for sqlalchemy
+- notebooks
|  - exp_data_analysis.ipynb - (extra) data analysis for all dataset
|  - run_query_and_perform_basic_data_analysis.ipynb - equivalent to app.py. to run all steps in interactive mode
+- pv- directory to keep persistent data (Docker)
|  +- augmented (all augmented images and json files will be written here)
|  +- data  
|    +- fashion-small (!need to be downloaded from kaggle!)
|       +- images
|       +- styles.csv
+- tests
|   - unit_test.py - Unit tests for app
+- utils
|  - FashionNetVgg16NoBn.py - model class 
|  - ImageAugmentation.py - image augmentation operations
|  - ModelInference.py - model inference file for deep-fashion-net
|  - S3Handler.py - s3 operations class
+- app.py 
+- init_db.py - create database and tables
+- init_task.py - submit sample task
+- load_data_to_db.py - load data from csv to postgres
+- README.md 
+- requirements.txt
```

# &nbsp;

## License
[MIT](https://choosealicense.com/licenses/mit/)
