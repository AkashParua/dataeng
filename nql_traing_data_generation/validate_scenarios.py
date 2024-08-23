import json
from jsonschema import validate
from typing import List

def validate_json_schema(json_string: str):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
            "name": {
                "type": "string"
            },
            "columns": {
                "type": "array",
                "items": {
                "type": "object",
                "properties": {
                    "name": {
                    "type": "string"
                    },
                    "type": {
                    "type": "string"
                    },
                    "constraints": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                    }
                },
                "required": ["name", "type"]
                }
            }
            },
            "required": ["name", "columns"]
        }
        }

    try:
        json_data = json.loads(json_string)
        validate(json_data, schema)
        return True
    except json.decoder.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return False


