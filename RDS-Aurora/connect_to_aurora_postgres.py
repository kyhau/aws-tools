"""
pip install aws-advanced-python-wrapper "psycopg[binary]"
"""

from aws_advanced_python_wrapper import AwsWrapperConnection
from psycopg import Connection

HOST = "TODO.rds.amazonaws.com"
DB_NAME = "TODO"
U_NAME = "TODO"
U_WHAT = "TODO"


with AwsWrapperConnection.connect(
    Connection.connect,
    f"host={HOST} dbname={DB_NAME} user={U_NAME} password={U_WHAT}",
    plugins="failover",
    wrapper_dialect="aurora-pg",
    autocommit=True,
) as awsconn:
    awscursor = awsconn.cursor()

    sql_statement = "SELECT aurora_db_instance_identifier()"
    print(sql_statement)
    awscursor.execute(sql_statement)
    awscursor.fetchone()
    for record in awscursor:
        print(record)

    sql_statement = "SELECT schema_name FROM information_schema.schemata;"
    print(sql_statement)
    awscursor.execute(sql_statement)
    schemas = awscursor.fetchall()
    for schema in schemas:
        print(schema)

    sql_statement = "SELECT nspname AS schema_name FROM pg_catalog.pg_namespace;"
    print(sql_statement)
    awscursor.execute(sql_statement)
    namespaces = awscursor.fetchall()
    for namespace in namespaces:
        print(namespace)

    sql_statement = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE';"
    print(sql_statement)
    awscursor.execute(sql_statement)
    tables = awscursor.fetchall()
    for table in tables:
        print(table)
