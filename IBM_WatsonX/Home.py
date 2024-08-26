import streamlit as st
import pandas as pd
from utils.utils import run_sql_query, result_to_df, generate_graph, pandas_dataframe_to_sqlite, init_sqlite_engine, fetch_all_tables, get_engine_metadata
from utils.llm_utils import load_config, init_llm, NQLengine, perform_nql_query
from sqlalchemy import text, create_engine
import os

def main():

    # Initialize session state variables
    if 'dataframes' not in st.session_state:
        st.session_state['dataframes'] = {}
    if 'keys_to_remove' not in st.session_state:
        st.session_state['keys_to_remove'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'queries' not in st.session_state:
        st.session_state['queries'] = []
    if 'result_df' not in st.session_state:
        st.session_state['result_df'] = None
    if 'engine' not in st.session_state:
        st.session_state['engine'] = create_engine('sqlite:///mydatabase.db', echo=False)  # Switch to file-based SQLite database
    
    conn = st.session_state['engine'].connect()
    st.write(get_engine_metadata(conn))
    
    granite_llm, embed_model = init_llm()
    query_engine = NQLengine(st.session_state['dataframes'].keys(), st.session_state['engine'], granite_llm, embed_model)

    def remove_table(name: str):
        if name in st.session_state['dataframes']:
            del st.session_state['dataframes'][name]
        conn.execute(text(f"DROP TABLE IF EXISTS {name}"))
        if name in st.session_state['keys_to_remove']:
            st.session_state['keys_to_remove'].remove(name)

    st.title("Data Dungeon Lab ⛃")
    uploaded_file = st.file_uploader("Choose a CSV file 📤", type="csv")

    current_tables = fetch_all_tables(conn)
    for table in current_tables:
        st.write("Current tables:", table)

    if uploaded_file is not None:
        file_name = uploaded_file.name.replace('.csv', '').replace('(', '_').replace(')', '_').replace(' ', '_')
        if file_name in st.session_state['dataframes']:
            st.write(f"Dataframe with name {file_name} already exists")
        else:
            df = pd.read_csv(uploaded_file)
            st.session_state['dataframes'][file_name] = df
            pandas_dataframe_to_sqlite(df, file_name, conn)
            
            # Check if the table is created and data is inserted
            table_data = conn.execute(text(f"SELECT * FROM {file_name} LIMIT 5")).fetchall()
            st.write(f"Sample data from {file_name}:", table_data)
    
    for key, value in st.session_state['dataframes'].items():
        with st.container():
            st.write(f"Table Name: {key}")
            st.write(value)
            if st.button(f"Remove Table {key}"):
                st.session_state['keys_to_remove'].append(key)

    if st.session_state['keys_to_remove']:
        for key in st.session_state['keys_to_remove']:
            remove_table(key)

    st.title("DUNGEON MASTER 🧙")
    user_input = st.text_input("You:", key="Ask the Dungeon Master")

    if st.button("Send"):
        str_response, sql_query = perform_nql_query(user_input, query_engine)
        st.write(f"Generated SQL Query: {sql_query}")
        try:
            st.session_state['messages'].append(str_response)
            st.session_state['result_df'] = result_to_df(conn.execute(text(sql_query)).fetchall())
            st.session_state['queries'].append(sql_query)
        except Exception as e:
            st.write(f"Error executing query: {e}")
            st.session_state['queries'].append(f'Query failed due to {e}. Reword your query.')

    if st.session_state['result_df'] is not None:
        st.write(st.session_state['result_df'])

    for m, q in zip(st.session_state['messages'][::-1], st.session_state['queries'][::-1]):
        st.write(f"DM: {m}")
        st.write(f"SQL Query: {q}")

    if st.button("Clear Chat"):
        st.session_state['messages'] = []
        st.session_state['queries'] = []

    if st.button("Clear Data"):
        st.session_state['dataframes'] = {}
        st.session_state['keys_to_remove'] = []
        st.session_state['messages'] = []
        st.session_state['queries'] = []

if __name__ == "__main__":
    main()
