import logging.config

from flask import Flask, Blueprint
from flask_cors import CORS

from . import config
from .db import db
from open_budget_data_api.api.budget_api import ns as budget_ns
from open_budget_data_api.api.entity_api import ns as entity_ns
from open_budget_data_api.api.exemption_api import ns as exemption_ns
from open_budget_data_api.api.procurement_api import ns as procurement_ns
from open_budget_data_api.api.restplus import api
from open_budget_data_api.api.supports_api import ns as supports_ns

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

    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


initialize_app(app)

def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=config.FLASK_DEBUG)


if __name__ == "__main__":
    main()
