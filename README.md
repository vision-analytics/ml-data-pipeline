# Project Details
## ml-data-pipeline


# &nbsp;

# Usage

```

#start services
docker compose up

#open interactive shell inside container
docker-compose exec celery_worker /bin/bash

#init db
-> python3 init_db.py

#export data from csv to db
-> python3 load_data_to_db.py

#submit sample task
-> python3 init_task.py

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

# Work In Progress

### check deep-fashion-net model weights
### !need to increase performance for the s3 operations. 
### TODO: Use aws cli with batch operations
    
    #*Note: current throughput 8-9 items/s 
    #*batch data upload with AWS CLI tool
    ```
    aws s3 sync local_folder s3://bucket-name
    ```

# 1 - setup database
```
    init_db.py
    load_data_to_db.py
```

# 2 - run query and export data
```
    app.py -> run_query
    app.py -> read_query_results
```

# 3 - jupyter - basic data analysis
```
    jupyter notebook notebooks/run_query_and_perform_basic_data_analysis.ipynb
```

# 4 - augmentations
```
    app.py -> run_augmentations
```
# 5 - run pretrained model
```
    app.py -> run_model_inference
```


# (extra) - Exploratory Data Analysis
```
jupyter notebook notebooks/exp_data_analysis.ipynb
```


### bonus - celery (will be implemented soon!)

# &nbsp;

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

# &nbsp;

#### Tested with following environments

##### Ubuntu 18.04 & python3.6

##### macOS Mojave 10.14.5 & python 3.6


# &nbsp;
# &nbsp;
# &nbsp;
# &nbsp;


# Old Setup Instructions(not used anymore)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
python3 -m venv test-env #create new environment
source test-env/bin/activate #activate environment
pip3 install -r requirements.txt
```


## run postgres (docker)
```
mkdir pv # create directory to keep persistent data(postgres)
docker-compose up
```

## setup env
```
cd <app root folder>

export PYTHONPATH="$PWD"
export POSTGRES_PWD=""
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_REGION_NAME=""
export AWS_BUCKET_NAME=""
```

### init db
```
python3 init_db.py
```

### load data to db
```
python3 load_data_to_db.py
```

### run app.py to go over all steps in order. Alternatively, you can use notebooks/run_query_and_perform_basic_data_analysis.ipynb.
```
python3 app.py
```

# &nbsp;
