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

Browse to [http://localhost:8888/graphql](http://localhost:8888/graphql)

#### Build package
```
python setup.py build
```

#### Build Docker
```
docker build .
```

#### Graphql
Example of a graphql query:
```
{
  budget(first: 10, year: 2016, where: "code like '002041%'", orderBy: "-net_allocated") {
    edges {
      node {
        code, year, title, netAllocated
        supports {
          edges {
            node {
              subject, title, amountAllocated, 
              entity {
                name, companyAddress
              }
            }
          }
        }                  
      }
    }
  }
}
```
## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
