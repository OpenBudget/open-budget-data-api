import logging.config

from flask import Flask, Blueprint
from flask_cors import CORS
from flask_graphql import GraphQLView

from . import config
from .db import db
from .api.budget_api import ns as budget_ns
from .api.budget_graphql import scheme
from .api.changes_api import ns as changes_ns
from .api.entity_api import ns as entity_ns
from .api.exemption_api import ns as exemption_ns
from .api.procurement_api import ns as procurement_ns
from .api.restplus import api
from .api.supports_api import ns as supports_ns

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = config.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = config.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = config.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = config.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = config.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    api.add_namespace(budget_ns)
    api.add_namespace(entity_ns)
    api.add_namespace(procurement_ns)
    api.add_namespace(exemption_ns)
    api.add_namespace(supports_ns)
    api.add_namespace(changes_ns)

    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=scheme,
            graphiql=True  # for having the GraphiQL interface
        )
    )


initialize_app(app)
