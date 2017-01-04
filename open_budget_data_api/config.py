import os

from playhouse.postgres_ext import PostgresqlExtDatabase

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PWD = os.environ.get('DB_PWD')
DB_DB = os.environ.get('DB_DB')

database = PostgresqlExtDatabase(host=DB_HOST, port=DB_PORT,
                                 user=DB_USER, password=DB_PWD,
                                 database=DB_DB,
                                 threadlocals=True, register_hstore=False)
