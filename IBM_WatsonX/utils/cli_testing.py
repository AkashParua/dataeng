import pandas as pd
from utils.llm_utils import load_config, init_llm, NQLengine, perform_nql_query
from utils.utils import run_sql_query, result_to_df, generate_graph, pandas_dataframe_to_sqlite
def main():
    df = pd.read_csv('utils/demo_data.csv')
    conn, engine = pandas_dataframe_to_sqlite(df, 'demo_data')
    granite_llm, embed_model = init_llm()
    query_engine = NQLengine(['demo_data'], engine, granite_llm, embed_model)
    query = "Find all the records with more than 5000 'orders' in the table 'demo_data'"
    str_response, sql_query = perform_nql_query(query, query_engine)
    print(str_response)
    print(sql_query)
    conn.close()

if __name__ == '__main__':
    main()