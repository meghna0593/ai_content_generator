import json
from src.constants import ORIGINAL_DATA_PROCESSED_FILE_PATH
from src.utils import fetch_data, store_data


def dfs_extract(json_obj, inner_most_text):
    if isinstance(json_obj, dict):
        # to extract the innermost text
        if "guid" in json_obj and "type" in json_obj:
            if "options" in json_obj and isinstance(json_obj["options"], dict):
                if json_obj["type"] == "LpTextReact":
                    if json_obj["options"]["doc"]["content"][0]["type"] in ("paragraph", "headline"):
                        for content in json_obj["options"]["doc"]["content"][0]["content"]:
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


def extract_original_text(file_path):
    data = fetch_data(file_path)
    processed_original_data = []

    # iterating section-wise
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

    store_data(processed_original_data, ORIGINAL_DATA_PROCESSED_FILE_PATH)
    return processed_original_data
