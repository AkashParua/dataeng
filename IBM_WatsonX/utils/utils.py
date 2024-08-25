from sqlalchemy import (create_engine, MetaData,
                        Table, Column, String, Integer)
from sqlalchemy.engine.base import Connection, Engine
import pandas as pd
from plotly.graph_objs import Figure
from typing import List, Tuple
import plotly.express as px
from sqlalchemy import text
import sqlglot


def extract_tables(sql_query: str) -> list:
    """
    Find all instances of tables in a sql query.
    """
    parsed = sqlglot.parse_one(sql_query)
    tables = parsed.find_all(sqlglot.expressions.Table)
    table_names = [table.name for table in tables]
    return table_names


def pandas_dataframe_to_sqlite(df: pd.DataFrame, table_name: str) -> tuple[Connection, Engine]:
    """
    This function takes a pandas dataframe and saves it to ain memory sqlite database.
    Args:
        df: pandas dataframe
        table_name: name of the table
    """
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    conn = engine.connect()
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    return conn, engine


def sqlite_to_pandas_dataframe(conn: Connection, table_name: str) -> pd.DataFrame:
    """
    This function takes a sqlite database and reads it into a pandas dataframe.
    Args:
        conn: sqlite connection
        table_name: name of the table
    """
    query = f'SELECT * FROM {table_name}'
    df = pd.read_sql(query, conn)
    return df


def run_sql_query(conn: Connection, query: str) -> List[Tuple]:
    """
    This function takes a sqlite connection and a query and returns the result.
    Args:
        conn: sqlite connection
        query: sql query
    Returns:
        result: result of the query in a list of tuples
    """
    result = conn.execute(text(query)).fetchall()
    return result


def result_to_df(result: List[Tuple]) -> pd.DataFrame:
    """
    This function takes a result from a sql query and returns it in a pandas dataframe.
    Args:
        result: result of the query in a list of tuples
    Returns:
        df: pandas dataframe
    """
    keys = [col[0] for col in result]
    values = [list(row[1:]) for row in result]
    dict_result = {k: v for k, v in zip(keys, values)}
    df = pd.DataFrame(dict_result)
    df = pd.DataFrame(result)
    return df


def generate_graph(df: pd.DataFrame, x: str, y: str, title: str, x_label: str, y_label: str, type: str = 'line') -> Figure:
    """
    This function takes a pandas dataframe and generates a plotly graph.
    Args:
        df: pandas dataframe
        x: x-axis column
        y: y-axis column
        title: title of the graph
        x_label: x-axis label
        y_label: y-axis label
    Returns:
        fig: plotly figure
    """
    if type == 'line':
        fig = px.line(df, x=x, y=y, title=title,
                      labels={x: x_label, y: y_label})
    elif type == 'bar':
        fig = px.bar(df, x=x, y=y, title=title,
                     labels={x: x_label, y: y_label})
    elif type == 'scatter':
        fig = px.scatter(df, x=x, y=y, title=title,
                         labels={x: x_label, y: y_label})
    elif type == 'histogram':
        fig = px.histogram(df, x=x, title=title, labels={
                           x: x_label, y: y_label})
    elif type == 'box':
        fig = px.box(df, x=x, y=y, title=title,
                     labels={x: x_label, y: y_label})
    return fig


def generate_mermaid_graph(existing_graph: str, query: str, table_created: str) -> str:
    """
    This function takes an existing mermaid graph and adds a new table to it.
    Args:
        existing_graph: existing mermaid graph
        query: sql query
        table_created: name of the table created
    """
    tables = extract_tables(query)
    tables = list(set(tables))
    for table in tables:
        existing_graph += f'{table} --> {table_created}\n'
    return existing_graph


if __name__ == '__main__':
    df = pd.read_csv('train.csv')
    conn, engine = pandas_dataframe_to_sqlite(df, 'test')
    df = sqlite_to_pandas_dataframe(conn, 'test')
    print(df.head())
    print(run_sql_query(conn, 'SELECT * FROM test;'))
    print(result_to_df(run_sql_query(conn, 'SELECT * FROM test;')))
    print(extract_tables('SELECT * FROM test;'))
    fig = generate_graph(df, 'date', 'orders',
                         'date-v-orders', 'date', 'orders', 'line')
    conn.close()
