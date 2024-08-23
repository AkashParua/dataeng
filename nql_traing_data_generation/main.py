import generate_scenarios, genrate_sql, validate_sql, validate_scenarios, utils
import yaml
# Load configuration from a YAML file
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

def main():
    num_samples = config["samples_per_request"]
    for i in range(500):
        samples = generate_scenarios.generate_sql_query_scenarios(num_samples)
        for sample in samples:
            try:
                instruction, schema = utils.extract_instruction_and_input(sample)
            except Exception as e:
                print(f"Error: {e}")
                continue
            is_schema_valid = validate_scenarios.validate_json_schema(schema)
            if is_schema_valid:
                sql_query = genrate_sql.generate_sql_query_samples(instruction, schema)
                is_query_valid = validate_sql.validate_queries(schema, sql_query)
        
                if is_query_valid:
                    print(f"Scenario is valid.")
                    with open('data.txt', 'a') as file:
                        file.write(f"{instruction}\n")
                        file.write(f"Schema:\n{schema}\n")
                        file.write(f"Response:\n{sql_query}\n")
                        file.write("------------------\n")
                else:
                    print(f"Query is invalid.")
            else:
                print(f"Schema for is invalid.")

if __name__ == "__main__":
    main()