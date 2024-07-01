from src.text_extraction import extract_text_from_json
from src.text_generation import generate_content, generate_related_content


def main():

    input_file_path = "data/input/test.json"
    data = extract_text_from_json(input_file_path)
    # generate_content(len(data["headline"]), len(data["paragraph"]), len(data["LpButtonReact"]))
    generate_related_content(data)


if __name__ == "__main__":
    main()
