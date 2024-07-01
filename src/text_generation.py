from dotenv import load_dotenv
import json
from openai import OpenAI
import os
from src.constants import AI_GENERATED_DATA_RAW_FILE_PATH, AI_GENERATED_DATA_PROCESSED_FILE_PATH
from src.utils import fetch_data, store_data

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPEN_AI_ORG_ID"))


# Generates new content using OpenAI API
def __ai_content_generator(prompt, count):
    responses = []
    attempts = 0
    max_attempts = 5

    while len(responses) < count and attempts < max_attempts:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=150, temperature=0.8, n=1
        )

        if response.choices[0].text.startswith("?"):  # removing bad character
            response.choices[0].text = response.choices[0].text[1:].strip()
        response = response.to_dict()
        try:
            response = json.loads(response["choices"][0]["text"].strip())
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            attempts += 1
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            attempts += 1
            continue

        responses.append(response)
    if len(responses) < count:
        print(f"Only {len(responses)} valid responses generated out of {count} requested.")
    return responses[:count]  # making sure we return the exact no.of content we need


# reformatting new content to match the original processed data
def reformat_content(data):
    res = []
    for item in data:  # format new content
        res.append(
            {
                "section_name": item["section_name"],
                "new_content": {
                    "headline": [
                        {"text": line["headline"], "id": id}
                        for id, line in enumerate(item["new_content"])
                        if "headline" in line.keys() and line["headline"]
                    ],
                    "paragraph": [
                        {"text": line["paragraph"], "id": id}
                        for id, line in enumerate(item["new_content"])
                        if "paragraph" in line.keys() and line["paragraph"]
                    ],
                    "LpButtonReact": [
                        {"text": line["button"], "id": id}
                        for id, line in enumerate(item["new_content"])
                        if "button" in line.keys() and line["button"]
                    ],
                },
            }
        )
    return res


def generate_content(data):
    result = []
    for item in data:
        prompt = f"A wellnessapp 'healthhub' helps users manage their health and fitness goals. It has a landing page with multiple sections. Generate a headline, a related paragraph, a button in a json format for the section {item['section_name']} healthhub"
        new_content = __ai_content_generator(prompt, max(item["inner_most_content"]["count"]))
        result.append({"section_name": item["section_name"], "new_content": new_content})
    store_data(result, AI_GENERATED_DATA_RAW_FILE_PATH)
    result = fetch_data(AI_GENERATED_DATA_RAW_FILE_PATH)
    final_result = reformat_content(result)
    store_data(final_result, AI_GENERATED_DATA_PROCESSED_FILE_PATH)
