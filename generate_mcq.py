import google.generativeai as genai
import json
import time

new_tem = []

def configure_genai(api_key):
    genai.configure(api_key=api_key)

def generate_mcqs(subject, num_mcqs, retries=5):
    model = genai.GenerativeModel('gemini-1.5-flash')
    mcqs = set()  # Use a set to store unique MCQs
    prompt_template = (
        f"Generate a unique multiple choice question on the topic '{subject}'. The format should be:\n\n"
        "Question: [question text]\n"
        "A) [option 1]\n"
        "B) [option 2]\n"
        "C) [option 3]\n"
        "D) [option 4]\n"
        "Correct Answer: [correct option letter]"
    )
    batch_size = 5  # Number of MCQs to request per call

    for attempt in range(retries):
        try:
            while len(new_tem) < num_mcqs:  # Continue until the required number of unique MCQs is reached
                response = model.generate_content(prompt_template)
                mcq_text = response.text.strip()
                start_index = mcq_text.index(':') + 1
                end_index = mcq_text.index('?')
                new_q = mcq_text[start_index:end_index].strip()
                if new_q not in new_tem:
                    new_tem.append(new_q)
                    if mcq_text not in mcqs:  # Check if MCQ is unique
                        mcqs.add(mcq_text)
                    print(f"Generated {len(new_tem)}/{num_mcqs} unique MCQs")
                    time.sleep(10)  # Small delay between batches to avoid immediate quota hit
                if len(new_tem) >= num_mcqs:
                    break
        except Exception as e:
            if "429 Resource has been exhausted" in str(e):
                print(e)
                if attempt < retries - 1:
                    wait_time = 60 * (attempt + 1)  # Exponential backoff
                    print(f"Quota exhausted. Retrying after {wait_time} seconds...")
                    time.sleep(wait_time)  # Wait longer after each attempt
                else:
                    raise
            else:
                raise e
        time.sleep(5)  # Small delay before retrying in case of other errors
    
    return list(mcqs)[:num_mcqs]  # Convert set to list and return required number of MCQs

def save_mcqs_to_json(mcqs, filename):
    with open(filename, 'w') as json_file:
        json.dump(mcqs, json_file, indent=4)

def main():
    api_key = input("Enter your Gemini API key: ")
    configure_genai(api_key)
    subject = input("Enter the subject: ")
    num_mcqs = int(input("Enter the number of MCQs: "))
    try:
        generated_mcqs = generate_mcqs(subject, num_mcqs)
        json_filename = f"{subject}_mcqs.json"
        save_mcqs_to_json(generated_mcqs, json_filename)
        print(f"\n{num_mcqs} MCQs on the topic '{subject}' have been generated and saved to {json_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
