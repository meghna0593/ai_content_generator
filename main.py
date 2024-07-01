from src.constants import INPUT_FILE_PATH
from src.text_extraction import extract_original_text
from src.text_generation import generate_content


def main():

    data = extract_original_text(INPUT_FILE_PATH)
    generate_content(data)


if __name__ == "__main__":
    main()
