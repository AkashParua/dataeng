from typing import List, Dict
import yaml
from utils import get_model_responses

def generate_sql_query_scenarios(num_samples: int) -> List[Dict[str, str]]:
    system_message = f"""You are an elite SQL expert AI, tasked with generating {num_samples} diverse and challenging SQL query scenarios for business analytics. Each scenario must be unique and designed to help train an AI model to generate SQL queries based on given table schemas.

    For each sample, provide:

    1. Instruction: A specific, challenging business analytics task that requires a SQL query.
    2. Input: 
        - Schema: A detailed schema of the relevant tables (list of tables with column names and data types, including primary and foreign keys) in JSON.
    
    Guidelines:
    - Cover a wide range of industries: tech, finance, retail, healthcare, education, etc.
    - Include various types of SQL queries: SELECT, JOIN, GROUP BY, subqueries, window functions, CTEs, etc.
    - Address different business objectives: sales analysis, customer segmentation, inventory management, financial forecasting, etc.
    - Incorporate different database structures: normalized schemas, star schemas, snowflake schemas, etc.
    - Consider various data challenges: large datasets, missing data, complex relationships, time-series analysis, etc.
    - Include challenging scenarios: complex joins, nested queries, data transformation, handling NULLs, etc.

    Format each sample as follows:
    
    ### Instruction:
    [Concise, specific SQL task]
    [Detailed business problem or analytical question]

    ### Input:
    Schema:
    [List of tables with columns, data types, primary keys, foreign keys]
    Please generate the schema in the following format:
    [
        {{
            "name": "customers",
            "columns": [
                {{"name": "customer_id", "type": "INT", "constraints": ["PRIMARY KEY"]}},
                {{"name": "name", "type": "VARCHAR(255)"}},
                {{"name": "email", "type": "VARCHAR(255)"}}
            ]
        }},
        {{
            "name": "orders",
            "columns": [
                {{"name": "order_id", "type": "INT", "constraints": ["PRIMARY KEY"]}},
                {{"name": "order_date", "type": "DATE"}},
                {{"name": "customer_id", "type": "INT", "constraints": ["FOREIGN KEY", "REFERENCES customers(customer_id)"]}}
            ]
        }}
    ]

    Saperatre each sample with '---'.

    Remember: Quality, complexity, and diversity are crucial. Each sample should be designed to push the boundaries of SQL query generation for business analytics."""

    user_message = f"Generate {num_samples} sophisticated and diverse SQL query scenarios that can be used to train a model for business analytics. Use the specified format, separating each sample with ---."

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    response = get_model_responses(messages)
    return [sample.strip() for sample in response.split("---") if sample.strip()]

# if __name__ == "__main__":
#     num_samples = config["samples_per_request"]
#     samples = generate_sql_query_scenarios(num_samples)
#     record_scenarios(samples)
    
