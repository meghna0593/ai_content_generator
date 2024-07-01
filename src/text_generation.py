from dotenv import load_dotenv
import json
from openai import OpenAI
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPEN_AI_ORG_ID"))


# Function to generate content using OpenAI API
def __ai_content_generator(prompt, count):
    responses = []
    attempts = 0
    max_attempts = 5

    while len(responses) < count and attempts < max_attempts:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=150, temperature=0.8, n=1
        )

        if response.choices[0].text.startswith("?"):
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
    return responses[:count]


# Store generated content
def store_content(new_content_raw, file_path):  # try catch block
    with open(file_path, "w+") as json_file:  # change name
        json.dump(new_content_raw, json_file, indent=4)


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


def generate_content(headline_count=1, paragraph_count=1, button_count=1):
    prompts = {
        "headline": "Generate different headlines for a wellness app called 'HealthHub' that helps users manage their health and fitness goals. Each headline should be engaging and related to health and wellness.",
        "paragraph": "Generate different paragraphs for a wellness app called 'HealthHub'. Each paragraph should highlight different features and benefits of the app, and should be engaging and informative and related to the headline.",
        "button": "Generate different call-to-action button texts for a wellness app called 'HealthHub'. Each button text should encourage users to start their health journey with the app.",
    }

    # Generate new content for each type of prompt #TODO: use asyncio
    # new_headlines = [__ai_content_generator(prompts["headline"]) for _ in range(headline_count)]
    # new_paragraphs = [__ai_content_generator(prompts["paragraph"]) for _ in range(paragraph_count)]
    # new_button_texts = [__ai_content_generator(prompts["LpButtonReact"]) for _ in range(button_count)]

    new_headlines = __ai_content_generator(prompts["headline"], headline_count)
    new_paragraphs = __ai_content_generator(prompts["paragraph"], paragraph_count)
    new_button_texts = __ai_content_generator(prompts["button"], button_count)

    store_content(new_headlines, new_paragraphs, new_button_texts)


"""
1. Ignore footer
2. The wellnessapp 'healthhub' helps users manage their health and fitness goals. It has a landing page with multiple sections. Generate a headline and a related paragraph for the section {section_name}"
"""


def fetch_data(json_file_path):
    try:
        with open(json_file_path, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError as e:
        print(e.strerror)
        exit(1)  # check this


def generate_related_content(data):
    result = []
    for item in data:
        prompt= f"A wellnessapp 'healthhub' helps users manage their health and fitness goals. It has a landing page with multiple sections. Generate a headline, a related paragraph, a button in a json format for the section {item["section_name"]} healthhub"
        new_content = __ai_content_generator(prompt, max(item["inner_most_content"]["count"]))
        result.append({"section_name":item["section_name"], "new_content":new_content})
    store_content(result, "./resources/ai_generated_page_content_raw.json")
    result = fetch_data("./resources/ai_generated_page_content_raw.json")
    final_result = reformat_content(result)
    store_content(final_result, "./resources/ai_generated_page_content.json")
