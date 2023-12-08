import json

def load_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def format_and_save_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Replace 'odds_data.json' with the path to your JSON file
json_file_path = 'odds_data.json'

# Load and process your data
loaded_data = load_json_file(json_file_path)

# Perform additional processing if needed...

# Format and save the data back to the file
format_and_save_json(json_file_path)