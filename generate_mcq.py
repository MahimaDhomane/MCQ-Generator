import google.generativeai as genai
import json
import re
import time

new_tem = []

def configure_genai(api_key):
    genai.configure(api_key=api_key)

def tokenize(text):
    return set(re.findall(r'\w+', text.lower()))

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0  # Return 0 if the union is zero to avoid division by zero
    return intersection / union

def generate_mcqs(subject, diff_level, num_mcqs, retries=5):
    model = genai.GenerativeModel('gemini-pro')
    mcqs = set()  # Use a set to store unique MCQs
    prompt_template = (
        f"Generate {num_mcqs} unique multiple choice questions of difficulty level '{diff_level}' on the topic '{subject}'. The format should be:\n\n"
        "Question: [question text]\n"
        "A) [option 1]\n"
        "B) [option 2]\n"
        "C) [option 3]\n"
        "D) [option 4]\n"
        "Correct Answer: [correct option letter]"
    )
    batch_size = num_mcqs  # Number of MCQs to request per call
    for attempt in range(retries):
        try:
            while len(new_tem) < num_mcqs:  # Continue until the required number of unique MCQs is reached
                response = model.generate_content(prompt_template)
                mcq_texts = response.text.strip().split("\n\n")
                for mcq_text in mcq_texts:
                    if mcq_text.strip() == "":
                        continue
                    try:
                        start_index = mcq_text.index(':') + 1
                        end_index = mcq_text.index('?')
                        new_q = mcq_text[start_index:end_index].strip()
                    except ValueError:
                        # Skip this MCQ if the expected substrings are not found
                        continue
                    new_q_tokens = tokenize(new_q)
                    is_similar = False
                    for existing_q in new_tem:
                        existing_q_tokens = tokenize(existing_q)
                        similarity = jaccard_similarity(new_q_tokens, existing_q_tokens)
                        if similarity > 0.8:
                            is_similar = True
                            break
                    if not is_similar:
                        new_tem.append(new_q)
                        if mcq_text not in mcqs:  # Check if MCQ is unique
                            mcqs.add(mcq_text)
                        print(f"Generated {len(new_tem)}/{num_mcqs} unique MCQs")
                    if len(new_tem) >= num_mcqs:
                        break
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
        time.sleep(1)  # Small delay before retrying in case of other errors
    return list(mcqs)[:num_mcqs]  # Convert set to list and return required number of MCQs

def save_mcqs_to_txt(mcqs, filename):
    with open(filename, 'w') as txt_file:
        for mcq in mcqs:
            txt_file.write(mcq + '\n\n')

def main():
    api_key = input("Enter your Gemini API key: ")
    configure_genai(api_key)
    subject = input("Enter the topic: ")
    num_mcqs = int(input("Enter the number of MCQs: "))
    diff_level = input("Enter the difficulty level of questions: ")
    try:
        generated_mcqs = generate_mcqs(subject, diff_level, num_mcqs)
        txt_filename = f"{subject}_mcqs.txt"
        save_mcqs_to_txt(generated_mcqs, txt_filename)
        print(f"\n{num_mcqs} MCQs on the topic '{subject}' have been generated and saved to {txt_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
