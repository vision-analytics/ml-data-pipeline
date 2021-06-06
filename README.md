# Project Details
## ml-data-pipeline


# &nbsp;

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
python3 -m venv test-env #create new environment
source test-env/bin/activate #activate environment
pip3 install -r requirements.txt
```

# &nbsp;

# Usage

## 1 - Setup DB

## run postgres (docker)
```
mkdir pv # create directory to keep persistent data(postgres)
docker run --rm --name mldp-pg -e POSTGRES_PASSWORD=pass123 -d -p 5432:5432 -v pv:/var/lib/postgresql/data postgres
```

## setup env
```
cd <app root folder>

export PYTHONPATH="$PWD"
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



Structure:
```
.
+- api
|  - query.py - query operations and data upload
+- config
|  - Config.py - configuration module for keeping variables
|  - list_attr_cloth.txt - Classes for deepfashion model
|  - list_category_cloth.txt - Classes for deepfashion model
+- data
|  +- fashion-small (!need to be downloaded from kaggle!)
|    +- images
|    - styles.csv
+- models
|  - Style.py - table structure for sqlalchemy
+- notebooks
|  - exp_data_analysis.ipynb - (extra) data analysis for all dataset
|  - run_query_and_perform_basic_data_analysis.ipynb - equivalent to app.py. to run all steps in interactive mode
+- pv - directory to keep persistent data (Docker)
+- tests
|   - unit_test.py - Unit tests for app
+- utils
|  - FashionNetVgg16NoBn.py - model class 
|  - ImageAugmentation.py - image augmentation operations
|  - ModelInference.py - model inference file for deep-fashion-net
|  - S3Handler.py - s3 operations class
+- app.py 
+- init_db.py - create database and tables
+- load_data_to_db.py - load data from csv to postgres
+- README.md 
+- requirements.txt
```


# &nbsp;

# Work In Progress

### deep-fashion-net model weights
### celery implementation
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