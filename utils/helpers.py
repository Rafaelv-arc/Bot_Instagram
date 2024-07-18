import json

def save_results_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
