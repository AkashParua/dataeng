import yaml
from typing import List
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
)
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from llama_index.llms.ibm import WatsonxLLM
from llama_index.embeddings.ibm import WatsonxEmbeddings
from llama_index.core import SQLDatabase
from sqlalchemy.engine.base import Connection, Engine
from llama_index.core import Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine

def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)


def init_llm() -> tuple[WatsonxLLM, WatsonxEmbeddings]:
    config_file_path = 'config/config.yaml'
    config = load_config(config_file_path)

    parameters = {
        GenTextParamsMetaNames.DECODING_METHOD: "sample",
        GenTextParamsMetaNames.STOP_SEQUENCES: ['\n\n']
    }
    granite_llm = WatsonxLLM(
        model_id='ibm/granite-13b-chat-v2',
        url=config['url'],
        apikey=config['apikey'],
        project_id=config['project_id'],
        temperature=0.2,
        max_new_tokens=100,
        additional_params=parameters
    )
    embed_model = WatsonxEmbeddings(apikey=config['apikey'], url=config['url'],
                                    model_id="ibm/slate-125m-english-rtrvr", project_id=config['project_id'])
    return granite_llm, embed_model

def NQLengine(table_names: List[str], engine : Engine, watson_llm: WatsonxLLM, watson_embed: WatsonxEmbeddings) -> NLSQLTableQueryEngine:
    sql_database = SQLDatabase(engine, include_tables=table_names)
    Settings.llm = watson_llm
    Settings.embed_model = watson_embed
    query_engine = NLSQLTableQueryEngine(sql_database)
    return query_engine

def perform_nql_query(query: str, query_engine: NLSQLTableQueryEngine) -> List[str]:
    response = query_engine.query(query)
    str_response = response.response
    sql_query = response.metadata['sql_query']
    return str_response, sql_query

