import argparse
import os 
from datetime import datetime
import json
import csv
import tempfile
import subprocess

# argparse Helper Functions
def csv_file_type(file_path):
    if not file_path.endswith('.csv') or not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' is not a valid CSV file.")
    return file_path

def json_file_type(file_path):
    if not file_path.endswith('.json') or not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' is not a valid JSON file.")
    return file_path

def collection_file_type(file_path):
    if not file_path.endswith('.postman_collection.json') or not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' is not a valid POSTMAN Collection file.")
    return file_path

def globals_file_type(file_path):
    if not file_path.endswith('.postman_globals.json') or not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' is not a valid POSTMAN Globals file.")
    return file_path

def environment_file_type(file_path):
    if not file_path.endswith('.postman_environment.json') or not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' is not a valid POSTMAN Environment file.")
    return file_path

def directory_type(dir_path):
    if not os.path.isdir(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            raise argparse.ArgumentTypeError(f"Unable to create directory: '{dir_path}'")
    return dir_path

def file_type(file_path):
    dir_path = get_path(file_path)
    if not os.path.isdir(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError:
            raise argparse.ArgumentTypeError(f"Unable to create directory: '{dir_path}'")
    return file_path

# Base64 Helper Functions
def json_file_path_to_dict(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def csv_file_path_to_list_list_str(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        csv_list = [[cell.replace(' ', '') for cell in row] for row in reader]
    return csv_list

def dict_to_json_temp_file_path(data):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        json.dump(data, tmp)
        temp_file_path = tmp.name
    return temp_file_path

def list_list_str_to_csv_temp_file_path(data):
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        writer = csv.writer(tmp)
        writer.writerows(data)
        temp_file_path = tmp.name
    return temp_file_path

def export_collection(col, name, directory):
    with open(directory + '/' + name + '.postman_collection.json', 'w') as postman_collection:
        postman_collection.write(json.dumps(col.collection.content, indent=4))
    with open(directory + '/' + name + '.postman_environment.json', 'w') as postman_environment:
        postman_environment.write(json.dumps(col.environment.content, indent=4))
    with open(directory + '/' + name + '.postman_globals.json', 'w') as postman_globals:
        postman_globals.write(json.dumps(col.globals.content, indent=4))
    if col.data.content:
        with open(directory + '/' + name + '.csv', 'w') as postman_data:
            writer = csv.writer(postman_data)
            writer.writerows(col.data.content)
    return 0

def create_backup_path(path):
    dir_name = os.path.dirname(path)
    file_name, ext = os.path.splitext(os.path.basename(path))
    new_file_name = f"{file_name}_backup{ext}"
    new_path = os.path.join(dir_name, new_file_name)
    return new_path

# Reporting Helper Functions
def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M")

# File Helper Functions
def get_file_name(file_path):
    return os.path.basename(file_path)

def get_path(file_path):
    return os.path.dirname(file_path)
    
def execute_command(command):
    print(f"EXECUTING : {command}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    return process.poll()