from playhouse.postgres_ext import PostgresqlExtDatabase

database = PostgresqlExtDatabase(host='data.obudget.org', port=5432,
                                 user='redash_reader', password='kaedusha',
                                 database='obudget',
                                 threadlocals=True, register_hstore=False)
