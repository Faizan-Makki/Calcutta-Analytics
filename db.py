import pyodbc

database = "assignments"
server = "LAPTOP-GRA2K3HI"

conn_str = (
    f"driver={{odbc driver 17 for sql server}};"
    f"database={database};"
    f"server={server};"
    f"trusted_connection=yes;"
)

# conn = pyodbc.connect(conn_str)
# curr = conn.cursor()
# conn.close()
# if not conn.closed:
#     print("Connection is locally open")
# else:
#     print("Connection has been closed")

def get_connection():
    conn = pyodbc.connect(conn_str)
    print("Connection is locally open")
    return conn


def close_connection(conn):
    conn.close()
    print("Connection closed")