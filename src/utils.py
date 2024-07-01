import json


def fetch_data(json_file_path):
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(e.strerror)
        exit(1)


def store_data(data, file_path):
    try:
        print(file_path)
        with open(file_path, "w+") as json_file:
            json.dump(data, json_file, indent=4)
    except FileNotFoundError as e:
        print(e.strerror)
        exit(1)
