import json
from jsonschema import validate, ValidationError

def validate_json(data):
    """
    Validate a JSON string against the required schema.

    Parameters:
    data (str): The JSON string to validate.

    Returns:
    bool: True if the JSON data matches the schema, False otherwise.
    """

    # Define the expected schema
    schema = {
        "type" : "object",
        "properties" : {
            "instruction": {"type" : "string"},
            "input" : {"type" : "string"},
            "output" : {"type" : "string"},
        },
        "required": ["input", "output"],
    }

    try:
        # Parse the JSON data
        json_data = json.loads(data)

        # Validate the JSON data
        validate(instance=json_data, schema=schema)

        # If no exception was raised by validate(), the JSON data is valid
        return True
    except (json.JSONDecodeError, ValidationError):
        # If a JSONDecodeError or ValidationError was raised, the JSON data is invalid
        return False

def validate_jsonl(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    print(f"Invalid record: {line}")
                    return False
                keys = ['instruction', 'input', 'output']
                if not all(key in data and isinstance(data[key], str) for key in keys):
                    print(f"Invalid record: {line}")
                    return False
            except json.JSONDecodeError:
                print(f"Line is not valid JSON: {line}")
                return False
    return True