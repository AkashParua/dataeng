from typing import List, Dict
from utils import get_model_responses

def generate_sql_query_samples(instruction: str, schema: str) -> str:
    system_message = f"""
     You are an advanced SQL query generation AI. Your task is to generate an accurate SQL query based on the following scenario.
        The scenario provides an instruction, a table schemas in JSON format, and a business problem. Your SQL query should be efficient, accurate, and adhere to best practices.

        ### Instruction:
        {instruction}

        ### Schema:
        {schema}

        Please generate the SQL query that fulfills the instruction based on the provided schema and context. The query should be formatted correctly and ready for execution in a SQLite environment.

        Format each sample as follows:

        ### Response:
        [SQL query that fulfills the instruction]

        Guidelines:
        - Do not include any formatting or comments in the response.
        - Generate ready to run SQL queries that fulfill the given instruction.
        - Return the response in plain text format.
        - DO NOT include the schema, any additional information or suggestion in the response


        Remember: Your query should be optimized for performance and correctness. Consider using appropriate SQL functions, clauses, and join conditions to achieve the desired result.
    """

    user_message = f"Generate an SQL query based on the provided instruction and schema. The query should be accurate and efficient."

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    response = get_model_responses(messages)
    return response.replace("## Response:", "").strip()