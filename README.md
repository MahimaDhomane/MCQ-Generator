# MCQ-Generator
MCQ Generator using Google Generative AI

**Project Goal**
- This Python script generates multiple-choice questions (MCQs) using the Google Generative AI API(gemini-pro). The script allows users to specify a topic, the number of MCQs to generate and the difficulty level of MCQs, and it saves the generated MCQs to a text file.

**Prerequisites**
- Google collab
- Google Generative AI API key

**Usage**
1. Clone this repository.
2. Run the script using on the google collab.
3. Enter your Google Generative AI API key when prompted.
4. Enter the subject for the MCQs.
5. Enter the number of MCQs to generate.
6. Enter the difficulty level for MCQs which should be given in range i.e. eg, easy to medium.
The script will generate the specified number of MCQs and save them to a txt file named <topic>_mcqs.txt

**Explanation**
1. Importing Libraries:
  - ```google.generativeai as genai```: Google Generative AI client library.
  - ```json```: For handling JSON file operations.
  - ```time```: For handling delays and retries.
  - ```re```:provides support for regular expressions.
  
2. Global Variables:
  - ```new_tem```: A list to keep track of unique question texts.

3. Functions:
  - `configure_genai(api_key)`: Configures the Google Generative AI client with the provided API key.
  - `jaccard_similarity(set1, set2)`: Calculates the Jaccard similarity between two sets.
  - `generate_mcqs(subject,diff_level, num_mcqs, retries=5)`: Generates a specified number of unique MCQs for a given subject, with retries for handling API quota limits.
  - `save_mcqs_to_txt(mcqs, filename)`: Saves the generated MCQs to a specified text file.
  - `main()`: The main function that executes the script and handles user inputs and outputs.

**Execution Flow**
1. The script starts with main().
2. The user is prompted for the API key, topic, number of MCQs and difficulty level.
3. configure_genai(api_key) sets up the API.
4. generate_mcqs(subject, num_mcqs) generates the MCQs.
   - a. Initialize the Model and Parameters: Inside generate_mcqs, the script initializes the model and prepares the prompt template, which specifies the format for the AI's response.
   - b. Request Generation from the AI: The script attempts to generate MCQs using the AI. It handles retries and checks for API rate limits.
   - c. Parse and Filter MCQs:The response from the AI is parsed, and the script checks each MCQ for uniqueness using the Jaccard similarity function. Unique questions are added to new_tem and mcqs.
6. save_mcqs_to_txt(mcqs, filename) saves the MCQs to a txt file.
7. Errors are caught and printed.
8. Completion and Notification: The script informs the user that the MCQs have been successfully generated and saved.
   
**Error Handling**
- The script includes basic error handling to manage issues such as API quota exhaustion, with exponential backoff retries.

**Note**
- Ensure you have a valid API key and sufficient quota.
- The script uses a small delay between requests to avoid hitting the rate limit.
- while giving the input for difficulty level use range. eg, easy to hard.
- This script is a basic example and can be further customized to fit your specific needs.
