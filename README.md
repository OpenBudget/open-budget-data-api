# Open Budget Data Api

[![Travis](https://img.shields.io/travis/OpenBudget/open-budget-data-api/master.svg)](https://travis-ci.org/OpenBudget/open-budget-data-api)
[![Coveralls](http://img.shields.io/coveralls/OpenBudget/open-budget-data-api.svg?branch=master)](https://coveralls.io/r/OpenBudget/open-budget-data-api?branch=master)

This is the API for the Open Budget data. You can perform Database Queries and download data


## Getting started

Create a virtual environment (if necessary) and install the requirements

```
pyvenv venv
source venv/bin/activate
pip install -r requirements.txt
```


# Set the Python Path
```
export PYTHONPATH=.:$PYTHONPATH
```

Instead of setting up the database locally, you can use a different database host

```
export DATABASE_URL=<db_url>
```
Check the current hosted database url 
At the time of writing it was `postgresql://readonly:readonly@data-next.obudget.org:5432/budgetkey`

Start app through ./start_server.sh
```
./start_server.sh
```

Now you can browse to the app, for example:
```
http://localhost:8000/api/query?query=select * from raw_budget
```

#### Build package
```
python setup.py build
```

#### Build Docker
```
docker build .
```

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
