import pdfplumber
import json
import re


# Define a function to extract information from the PDF
def extract_pdf_information(pdf_file):
    pdf_data = []
    question = {}
    is_question = False
    answers = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            # Split the page text into lines
            lines = page_text.split('\n')

            for line in lines:
                line = line.strip()
                # Check if the line contains question-related information
                if re.match(r"Question #[0-9]+\s+Topic \d+", line):
                    if question:
                        # Check if the question starts with "SIMULATION -"
                        if not question["Question"].startswith("SIMULATION -"):
                            question["Answers"] = answers
                            pdf_data.append(question)
                        answers = []
                    question = {
                        "Question Number": re.search(r"Question #(\d+)", line).group(1),
                        "Topic Number": re.search(r"Topic (\d+)", line).group(1),
                        "Question": "",
                        "Correct Answer": None,
                        "Community Vote Distribution": None,
                    }
                    is_question = True
                elif is_question:
                    if re.match(r"[A-Z]\. ", line):
                        answers.append(line)
                    elif line.startswith("Correct Answer: "):
                        temp = line.replace("Correct Answer: ", "")
                        question["Correct Answer"] = [char for char in temp]
                        is_question = False
                    else:
                        question["Question"] += line
                # if line contain% then it is community vote distribution
                elif "%" in line:
                    temp = line.split(' ')
                    question["Community Vote Distribution"] = [char for char in temp[0]]

    # Append the last question
    if question:
        # Check if the last question starts with "SIMULATION -"
        if not question["Question"].startswith("SIMULATION -"):
            question["Answers"] = answers
            pdf_data.append(question)

    return pdf_data


# Define the PDF file path
pdf_file_path = 'mb-300(10).pdf'

# Extract information from the PDF
questions_data = extract_pdf_information(pdf_file_path)

# Create a JSON file with the extracted information
json_file_path = 'questions_data(10).json'
with open(json_file_path, 'w') as json_file:
    json.dump(questions_data, json_file, indent=4)

print(f'Information extracted from {pdf_file_path} and saved to {json_file_path}.')
