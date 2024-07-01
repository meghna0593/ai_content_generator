import json
import shutil


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
        with open(file_path, "w+") as json_file:
            json.dump(data, json_file, indent=4)
    except FileNotFoundError as e:
        print(e.strerror)
        exit(1)


def clone_file(src, dest):
    try:
        shutil.copyfile(src, dest)
        print(f"File {src} has been cloned to {dest}")
    except Exception as e:
        print(f"Error cloning file: {e}")
