import re

from flask import Flask
from flask_restful import Api

from . import handlers
from .config import database

app = Flask(__name__)
api = Api(app)


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


def words(path):
    return re.findall('([a-z]+)', path.lower())

# resources = [
#     BudgetHandler
# ]
for resource in handlers.__dict__.values():
        try:
            if issubclass(resource, handlers.ObudgetResource):
                for path in resource.PATHS:
                    ep_name = resource.__name__.lower()
                    ep_name += '_'.join([''] + words(path))
                    print(path, ep_name)
                    api.add_resource(resource, '/api/' + path, endpoint=ep_name)
        except AttributeError:
            pass
        except TypeError:
            pass


# def serve():
#     app.run(debug=False)
#
# serve()
