## Initial set up
1. To activate virtual env (macOS):
```python
python3 -m venv myenv
source myenv/bin/activate
```
2. make install

3. Create .env file and add OpenAI API keys
>OPENAI_API_KEY=
>OPEN_AI_ORG_ID=

4. make execute

## Current Approach:
1. Extracted Original data in the following format (`src/text_extraction.py`):
```json
{
        "section_id": "",
        "section_name": "",
        "inner_most_content": {
            "headline": [
                {
                    "text": "",
                    "guid": ""
                }
            ],
            "paragraph": [
                {
                    "text": "",
                    "guid": ""
                }
            ],
            "LpButtonReact": [
                {
                    "text": "",
                    "guid": ""
                }
            ],
            "count": [] // [headline_count, paragraph_count, button_count]
        }
    }
```
Separated data into sections for ease of use and readability. Extracted each inner level’s guid for tracking components easily. Added a count of headlines, paragraphs, and buttons for each section to generate the correct amount of content for replacement.

2. Generated new content by passing a prompt with a dynamic value for `sections` (`src/text_generation.py`). We generate the headline, paragraph, and button together to ensure the received data is coherent. In case of a corrupt response, we perform up to 5 retries. The initial raw content is stored in `data/resources/ai_generated_page_content_raw.json`, and after further processing, the data is stored in `data/resources/ai_generated_page_content.json`.

3. Replace new content (`src/content_updation.py`): Workflow explained in the file.


## Future Updates:
- Expand the context beyond 'HealthHub' by implementing a prompt that generates a list of different contexts, enabling dynamic content creation for each.
- Enhance text extraction and AI prompts. The test.json file contains subhead, small-subhead, and lp_lists types, which are currently not addressed in the solution.
- Increase robustness by adding more try/catch blocks and checks to handle edge cases effectively. Improve error handling for scenarios where all responses from GPT-3.5-turbo-instruct are corrupt.
- Implement unit tests.

