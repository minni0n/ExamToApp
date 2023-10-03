import json

# Function to remove specified characters from a string
def remove_chars(text, chars):
    for char in chars:
        text = text.replace(char, '')
    return text

# Load the JSON file
with open('questions_data.json', 'r') as file:
    data = json.load(file)

# Define the characters to remove
characters_to_remove = ['\u0000', '\u2013']

# Recursively remove characters from a dictionary or a list
def remove_chars_from_data(data, chars):
    print(len(data))
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = remove_chars_from_data(value, chars)
        return data
    elif isinstance(data, list):
        return [remove_chars_from_data(item, chars) for item in data]
    elif isinstance(data, str):
        return remove_chars(data, chars)
    else:
        return data

# Remove characters from the JSON data
data = remove_chars_from_data(data, characters_to_remove)

# Write the modified JSON back to the file
with open('questions_data_output.json', 'w') as file:
    json.dump(data, file, indent=4)