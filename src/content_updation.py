import json
import shutil

"""
1. Clone the test.json file
1.a. Pull data from original page, iterate over each section
1.b. iterate over headline / pragraph / button and match it with the new generated content with its guid
2. Get a list of all guids of headline/paragrah/button 
3. iterate over the headline's guid and replace all headlines from generated... continue for others
"""


def clone_original(src, dest):  # not needed
    try:
        shutil.copyfile(src, dest)
        print(f"File {src} has been cloned to {dest}")
    except Exception as e:
        print(f"Error cloning file: {e}")


def get_file_data(file_path):
    try:
        # Read the existing data from the file
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    except Exception as e:
        print(f"An error occurred: {e}")


def get_clean_generated_ai_content():
    pass


def process_original_extracted_content():
    pass


def replace_new_content():
    # have the original file in a variable
    # have the new content in a variable
    # have all the ids
    pass


def extract_text_from_json(json_data, reference_data, new_data):
    updated_data = []
    for idx in range(len(json_data["boxes"])):
        pass
        # helper(json_data["boxes"][idx], reference_data[idx], new_data[idx])


def create_new_content():  # main entry point
    source_file = "./data/input/test.json"
    dest_file = "./data/output/result.json"
    resource_ai_clean_file = "./data/resources/ai_generated_page_content.json"
    resource_original_file = "./data/resources/original_page_content_processed.json"

    clone_original(source_file, dest_file)

    data_to_update = get_file_data(dest_file)
    reference_data = get_file_data(resource_original_file)
    new_data = get_file_data(resource_ai_clean_file)

    # new_content_clean = get_clean_generated_ai_content(resource_ai_file)
    # update_json_file(data_to_update, reference_data, new_data)
    extract_text_from_json(data_to_update, reference_data, new_data)


"""
go section by section from cloned data
take guid for that section from extracted data and 
"""
create_new_content()
