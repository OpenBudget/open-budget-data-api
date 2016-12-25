# oki-py

[![Travis](https://img.shields.io/travis/OpenBudget/open-budget-data-api/master.svg)](https://travis-ci.org/OpenBudget/open-budget-data-api)
[![Coveralls](http://img.shields.io/coveralls/OpenBudget/open-budget-data-api.svg?branch=master)](https://coveralls.io/r/OpenBudget/open-budget-data-api?branch=master)

{{ DESCRIPTION }}

## Documentation

{{ DOCUMENTATION }}

#### Getting started
```
# prepare env if needed
pyvenv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.:$PYTHONPATH

# start app
python rest/main.py
```

Browse to [http://localhost:8888/api](http://localhost:8888/api)

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
