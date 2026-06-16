from components.footer import show_footer
import streamlit as st
from services.database_service import connect_sql_server, get_tables
import pandas as pd

st.info(
    "Currently, only Microsoft SQL Server instances are supported. "
    "Please enter the server name of your local SQL Server installation "
    "(e.g., localhost, .\\SQLEXPRESS, or YOUR-PC\\SQLEXPRESS). "
    "SQL Server authentication and remote servers are not supported yet."
)


if "connected" not in st.session_state:
    st.session_state.connected = False

if "tablelist" not in st.session_state:
    st.session_state.tablelist = []

st.title("Connect to Database")


db_type = st.selectbox(
    "Database Type",
    ["SQL Server", "MySQL", "PostgreSQL", "SQLite"]
)

host = st.text_input("Host / Server")
database = st.text_input("Database Name")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# connect_btn = st.button("Connect")

if st.button("Connect") and db_type == "SQL Server":

    conn = connect_sql_server(
        host=host,
        database=database
    )

    if conn:
        st.session_state.connected = True
        st.session_state.host = host
        st.session_state.database = database

        tablelist_df = get_tables(conn)
        st.session_state.tablelist = tablelist_df["table_name"].tolist()

        st.success("Database connected successfully")

if st.session_state.connected:

    selected_table = st.selectbox(
        "Select Table",
        st.session_state.tablelist
    )

    if st.button("Load Table"):

        conn = connect_sql_server(
            host=st.session_state.host,
            database=st.session_state.database
        )

        st.session_state.main_df = pd.read_sql(
            f"SELECT * FROM [{selected_table}]",
            conn
        )
        if "data_source" not in st.session_state:
            st.session_state.data_source = "database"
       
if "main_df" in st.session_state:
    st.subheader("Table Data")
    st.dataframe(st.session_state.main_df, use_container_width=True)

show_footer()