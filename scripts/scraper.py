import json
from rich.panel import Panel

def load_json_data(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)

def prettify_json(input_file_path, output_file_path):
    with open(input_file_path, 'r') as json_file:
        json_object = json.load(json_file)
    
    with open(output_file_path, 'w') as write_file:
        json.dump(json_object, write_file, indent=4, sort_keys=True)

def copy_block(source_file, target_file, block_name):
    with open(source_file, 'r') as source:
        source_data = json.load(source)

    if block_name in source_data:
        block_to_copy = source_data[block_name]
    else:
        print(Panel(f"The block '{block_name}' does not exist in the source file."))
        return

    with open(target_file, 'w') as target:
        json.dump({block_name: block_to_copy}, target, indent=4)
