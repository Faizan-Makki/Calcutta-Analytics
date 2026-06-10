import pandas as pd
import sqlite3
import pyodbc
import pymysql
import psycopg2

def connect_sql_server(host, database, username=None, password=None):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={host};"
        f"DATABASE={database};"
        f"Trusted_connection=Yes;"
        # f"UID={username};"
        # f"PWD={password};"
    )

    return pyodbc.connect(conn_str)


def connect_mysql(host, database, username, password):
    return pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )

def connect_postgres(host, database, username, password):
    return psycopg2.connect(
        host=host,
        database=database,
        user=username,
        password=password
    )

def connect_sqlite(db_file):
    return sqlite3.connect(db_file)


def get_tables(conn):
    query = """
    SELECT table_name
    FROM information_schema.tables
    """

    return pd.read_sql(query, conn)


def load_table(conn, table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, conn)