import streamlit as st
import pandas as pd
from utils.utils import run_sql_query, result_to_df, generate_graph, pandas_dataframe_to_sqlite, init_sqlite_engine
from utils.llm_utils import load_config, init_llm, NQLengine, perform_nql_query
from sqlalchemy import text
import os

engine, conn = init_sqlite_engine()

def main():
    if 'dataframes' not in st.session_state:
        st.session_state['dataframes'] = {}
    if 'keys_to_remove' not in st.session_state:
        st.session_state['keys_to_remove'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'queries' not in st.session_state:
        st.session_state['queries'] = []
    if 'granite_llm' not in st.session_state and 'embed_model' not in st.session_state:
        st.session_state['granite_llm'], st.session_state['embed_model'] = init_llm()
    if 'query_engine' not in st.session_state:
        st.session_state['query_engine'] = NQLengine(st.session_state['dataframes'].keys(), engine, st.session_state['granite_llm'], st.session_state['embed_model'])


    def remove_table(name : str):
        if name in st.session_state['dataframes']:
            del st.session_state['dataframes'][name]
        conn.execute(text(f"DROP TABLE {name}"))

    st.title("Data Dungeon Lab ⛃")
    uploaded_file = st.file_uploader("Choose a CSV file 📤", type="csv")

    if uploaded_file is not None:
        file_name = uploaded_file.name.replace('.csv', '').replace('(', '_').replace(')', '_').replace(' ', '_')
        if file_name in st.session_state['dataframes']:
            st.write(f"Dataframe with name {file_name} already exists")
        else:
            df = pd.read_csv(uploaded_file)
            st.session_state['dataframes'][file_name] = df
            pandas_dataframe_to_sqlite(df, file_name, conn)
    
    for key, vlaue in st.session_state['dataframes'].items():
        with st.container(height=500):
            st.write(f"Table Name: {key}")
            st.write(vlaue)
            if st.button(f"Remove Table {key}"):
                st.session_state['keys_to_remove'].append(key)

    if st.session_state['keys_to_remove']:
        for key in st.session_state['keys_to_remove'] :
            remove_table(key)   
        st.session_state['keys_to_remove'] = []
    

    st.title("DUNGEON MASTER 🧙")
    user_input = st.text_input("You:", key="Ask the Dungeon Master")
    sql_query = None
    if st.button("Send"):
        str_response, sql_query = perform_nql_query(user_input, st.session_state['query_engine'])
        st.session_state['messages'].append(str_response)
        st.session_state['queries'].append(sql_query)
        result_df =  result_to_df(conn.execute(text(sql_query)).fetchall())
        st.write(result_df)
             
    for m, q in zip(st.session_state['messages'], st.session_state['queries']):
        st.write(f"DM: {m}")
        st.write(f"SQL Query: {q}")
    

    conn.close()
    if st.button("Clear Chat"):
        st.session_state['messages'] = []
        st.session_state['queries'] = []

    if st.button("Clear Data"):
        st.session_state['dataframes'] = {}
        st.session_state['keys_to_remove'] = []
        st.session_state['messages'] = []
        st.session_state['queries'] = []
        os.remove('database.db')
        st.session_state['granite_llm'], st.session_state['embed_model'] = init_llm()
        st.session_state['query_engine'] = NQLengine([], engine, st.session_state['granite_llm'], st.session_state['embed_model'])

if __name__ == "__main__":
    main()