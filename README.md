# MCQ-Generator
MCQ Generator using Google Generative AI

**Project Goal**
- This Python script generates multiple-choice questions (MCQs) using the Google Generative AI API(gemini-1.5-flash). The script allows users to specify a subject and the number of MCQs to generate, and it saves the generated MCQs to a JSON file.

**Prerequisites**
- Python 3.x
- Google Generative AI API key

**Usage**
1. Clone this repository.
2. Install the required dependency:
```sh
pip install google-generativeai
```
4. Run the script using 
```sh
python generate_mcq.py
```
5. Enter your Google Generative AI API key when prompted.
6. Enter the subject for the MCQs.
7. Enter the number of MCQs to generate.
The script will generate the specified number of MCQs and save them to a JSON file named <subject>_mcqs.json.

**Explanation**
1. Importing Libraries:
  - ```google.generativeai as genai```: Google Generative AI client library.
  - ```json```: For handling JSON file operations.
  - ```time```: For handling delays and retries.
  
2. Global Variables:
  - ```new_tem```: A list to keep track of unique question texts.

3. Functions:
  - configure_genai(api_key): Configures the Google Generative AI client with the provided API key.
  - generate_mcqs(subject, num_mcqs, retries=5): Generates a specified number of unique MCQs for a given subject, with retries for handling API quota limits.
  - save_mcqs_to_json(mcqs, filename): Saves the generated MCQs to a specified JSON file.
  - main(): Orchestrates the execution of the script.

**Execution Flow**
1. The script starts with main().
2. The user is prompted for the API key, subject, and number of MCQs.
3. configure_genai(api_key) sets up the API.
4. generate_mcqs(subject, num_mcqs) generates the MCQs.
5. save_mcqs_to_json(mcqs, filename) saves the MCQs to a JSON file.
6. Errors are caught and printed.
   
**Error Handling**
- The script includes basic error handling to manage issues such as API quota exhaustion, with exponential backoff retries.

**Note**
- Ensure you have a valid API key and sufficient quota.
- The script uses a small delay between requests to avoid hitting the rate limit.
- This script is a basic example and can be further customized to fit your specific needs.
