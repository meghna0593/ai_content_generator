import json


def fetch_raw_data(json_file_path):
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(e.strerror)
        exit(1)  # check this


def store_processed_data(extracted_data):
    try:
        with open("./resources/original_page_content_processed.json", "w+") as json_file:  # change name
            json.dump(extracted_data, json_file, indent=4)
    except FileNotFoundError as e:
        print(e.strerror)
        exit(1)  # check this


def dfs_extract(json_obj, inner_most_text):
    if isinstance(json_obj, dict):
        # to extract the innermost text
        if "guid" in json_obj and "type" in json_obj:
            if "options" in json_obj and isinstance(json_obj["options"], dict):
                if json_obj["type"] == "LpTextReact":
                    if json_obj["options"]["doc"]["content"][0]["type"] in ("paragraph", "headline"):
                        for content in json_obj["options"]["doc"]["content"][0]["content"]:
                            # results[json_obj["options"]["doc"]["content"][0]["type"]].append(content["text"])
                            inner_most_text[json_obj["options"]["doc"]["content"][0]["type"]].append(
                                {"text": content["text"], "guid": json_obj["guid"]}
                            )
                elif json_obj["type"] == "LpButtonReact":
                    inner_most_text[json_obj["type"]].append(
                        {"text": json_obj["options"]["text"], "guid": json_obj["guid"]}
                    )

        for key, value in json_obj.items():
            dfs_extract(value, inner_most_text)
    elif isinstance(json_obj, list):
        for item in json_obj:
            dfs_extract(item, inner_most_text)

    return inner_most_text


def extract_text_from_json(file_path):
    # Define the path to your JSON file # exception here
    data = fetch_raw_data(file_path)
    processed_original_data = []

    for box in data.get("boxes", []):
        if "boxes" in box:
            json_format = {"headline": [], "paragraph": [], "LpButtonReact": []}
            section_data = {"section_id": box["guid"], "section_name": box["name"]}

            section_data["inner_most_content"] = dfs_extract(box.get("boxes"), json_format)
            section_data["inner_most_content"]["count"] = (
                len(section_data["inner_most_content"]["headline"]),
                len(section_data["inner_most_content"]["paragraph"]),
                len(section_data["inner_most_content"]["LpButtonReact"]),
            )
            processed_original_data.append(section_data)

    store_processed_data(processed_original_data)

    return processed_original_data
