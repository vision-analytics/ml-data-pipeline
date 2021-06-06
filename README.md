# ml-data-pipeline

# &nbsp;

# 0 - Exploratory Data Analysis
```
jupyter notebook notebooks/exp_data_analysis.ipynb
```

# &nbsp;

# 1 - Setup DB

## run postgres (docker)
```
mkdir pv # create directory to keep persistent data(postgres)
docker run --rm --name mldp-pg -e POSTGRES_PASSWORD=pass123 -d -p 5432:5432 -v pv:/var/lib/postgresql/data postgres
```

## Export Data to DB
```
cd <app root folder>
export PYTHONPATH="$PWD"
```

### init db
```
python3 init_db.py
```

### load data to db
```
python3 load_data_to_db.py
```

# &nbsp;

# 2 - Query API & export result to s3
    +json

# 3 - jupyter - basic data analysis

# 4 - augmentations

# 5 - run pretrained model

# bonus - celery