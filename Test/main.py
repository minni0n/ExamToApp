import pdfplumber
import json


def extract_pdf_information(pdf_file):
    pdf_data = []
    question = {}
    is_question = False

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            print(page_text)
            # Split the page text into lines
            lines = page_text.split('\n')
            print(lines)
            for line in lines:
                line = line.strip()
                if line.startswith("Question #"):
                    if question:
                        pdf_data.append(question)
                    question = {
                        "Question Number": line.replace("Question #", "").split()[0],
                        "Topic Number": line.split()[-1],
                        "Question": "",
                        "Answers": [],
                        "Correct Answer": None,
                        "Community Vote Distribution": None,
                    }
                    is_question = True
                elif is_question:
                    if line.startswith("Correct Answer:"):
                        question["Correct Answer"] = line.replace("Correct Answer:", "").strip()
                    elif line.startswith("Community vote distribution"):
                        question["Community Vote Distribution"] = line.replace("Community vote distribution","").strip()
                    else:
                        question["Question"] += line + " "
                elif line.startswith("A. "):
                    question["Answers"].append(line[3:])

    # Append the last question
    if question:
        pdf_data.append(question)

    return pdf_data


# Define the PDF file path
pdf_file_path = '../working/mb-300(10).pdf'

# Extract information from the PDF
questions_data = extract_pdf_information(pdf_file_path)

# Create a JSON file with the extracted information
json_file_path = 'questions_data.json'
with open(json_file_path, 'w') as json_file:
    json.dump(questions_data, json_file, indent=4)

print(f'Information extracted from {pdf_file_path} and saved to {json_file_path}.')
