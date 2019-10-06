import os

# Flask settings
FLASK_SERVER_NAME = os.environ.get('SERVER_NAME', 'localhost:8888')
FLASK_DEBUG = True  # Do not use debug mode in production

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgresql://readonly:readonly@data-next.obudget.org:5432/budgetkey'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True  # Do not use debug mode in production
