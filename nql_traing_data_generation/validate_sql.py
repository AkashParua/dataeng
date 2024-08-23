from utils import generate_ddl_from_schema, run_query
import ast
from typing import List

def validate_queries(schema: str, dml_query: str) -> bool:
    schema =  ast.literal_eval(schema)
    ddl_queries = generate_ddl_from_schema(schema)
    try:
        for ddl in ddl_queries:
            run_query(ddl)
    except Exception as e:
        print(f"Error: {e}")
        return False
    try:
        run_query(dml_query)
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True


