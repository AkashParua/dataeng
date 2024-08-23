
from openai import OpenAI
from rich.console import Console as console
from typing import List, Dict
import time
import yaml
import os
import re
import sqlite3
# Initialize the AI/ML API client with your API key and base URL
PATH_TO_YAML = "config.yaml"

with open(PATH_TO_YAML, 'r') as config_file:
    config = yaml.safe_load(config_file)

client = OpenAI(
    api_key=config["api_key"],
    base_url="https://api.aimlapi.com",
)
# Load configuration from a YAML file
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def rate_limited_api_call(messages):
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=4096,
    )
    return response

def get_model_responses(messages: List[Dict[str, str]], max_retries: int = 3, timeout: int = 60) -> str:
    for attempt in range(max_retries):
        try:
            response = rate_limited_api_call(messages)
            return response.choices[0].message.content.strip()
        except Exception as e:
            console.print(f"[bold red] Error in the model response (Attempt {attempt + 1} / {max_retries}): {e} [/bold red]")
            if attempt < max_retries - 1:
                time.sleep(5)
    raise Exception("Failed to get the response after repeated errors")

def extract_instruction_and_input(content: str):
    print('///////////////////////////////////////////////')
    # Define regex patterns
    instruction_pattern = r"### Instruction:\s*(.*?)\s*### Input:"
    input_pattern = r"(?<=### Input:\n)(.*?)(?=$)"
    # Extract instruction
    instruction_matches = re.search(instruction_pattern, content, re.DOTALL).group(1).strip()
    # Extract input
    input_matches = re.search(input_pattern, content, re.DOTALL).group(1).replace("Schema:", "").strip()

    print(instruction_matches, input_matches)
    print('///////////////////////////////////////////////')
    return  instruction_matches, input_matches

def generate_ddl_from_schema(json_data: List[Dict[str, str]]) -> List[str]:
    sql_statements = []
    
    for table in json_data:
        table_name = table['name']
        columns = table['columns']
        
        # Create table statement
        create_table_sql = f"CREATE TABLE {table_name} ("
        
        # Column definitions
        column_definitions = []
        
        for column in columns:
            column_name = column['name']
            column_type = column['type']
            constraints = column.get('constraints', [])
            
            # Column definition
            column_definition = f"{column_name} {column_type}"
            
            # Add constraints if any
            if constraints:
                constraints_str = ', '.join(constraints)
                column_definition += f" {constraints_str}"
            
            column_definitions.append(column_definition)
        
        # Join column definitions
        column_definitions_str = ', '.join(column_definitions)
        
        # Finalize create table statement
        create_table_sql += column_definitions_str
        create_table_sql += ");"
        
        # Add create table statement to SQL statements list
        sql_statements.append(create_table_sql)
        
    return sql_statements

def run_query(content: str):
    db_path = 'db/database.db'
    print('QUERY:', content)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(content)
        conn.commit()  # Commit the transaction if it's a write operation
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            conn.close()
