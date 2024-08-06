import streamlit as st
import sqlite3
import pandas as pd

st.title("SQLite Database Viewer")

# Upload Database File
uploaded_file = st.file_uploader("Upload SQLite Database", type=["db", "sqlite", "sqlite3"])

if uploaded_file is not None:
    conn = sqlite3.connect(uploaded_file)
    cursor = conn.cursor()

    # Fetch table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]

    st.sidebar.header("Tables")
    selected_table = st.sidebar.selectbox("Select a table", table_names)

    # Display selected table data
    if selected_table:
        query = f"SELECT * FROM {selected_table}"
        df = pd.read_sql_query(query, conn)
        st.write(f"Displaying data for table: {selected_table}")
        st.dataframe(df)

        # Display schema of the selected table
        if st.sidebar.checkbox("Show Schema"):
            schema_query = f"PRAGMA table_info({selected_table})"
            schema_df = pd.read_sql_query(schema_query, conn)
            st.write("Schema of the table:")
            st.dataframe(schema_df)

        # SQL query execution
        if st.sidebar.checkbox("Run SQL Query"):
            user_query = st.text_area("Enter SQL Query", f"SELECT * FROM {selected_table} LIMIT 10")
            if st.button("Execute"):
                query_result = pd.read_sql_query(user_query, conn)
                st.write("Query Result:")
                st.dataframe(query_result)

