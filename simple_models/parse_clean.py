import string
import re
import random

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
# print(stopwords.words('english'))


def remove_unwanted_newlines(lines):
    cleaned_lines = []
    line_i = 0
    while (line_i < len(lines)):
        if lines[line_i][0] == " ":
            build_str = lines[line_i - 1]
            cleaned_lines.pop()
            while line_i < len(lines) and lines[line_i][0] == " ":
                build_str = build_str[:-1] # get rid of new line char at end
                build_str += lines[line_i]
                line_i += 1
            cleaned_lines.append(build_str)
            # cleaned_lines.append(lines[line_i])
        else:
            cleaned_lines.append(lines[line_i])
            line_i += 1
    
    return cleaned_lines
    # with open(output_file, "w") as file:
    #     file.writelines(cleaned_lines)


def rm_stop_words(line):
    # # Step 1: Split the sentence into words
    year = line[:4]
    state = line[5:7]
    abstract = line[8:]
    words = abstract.split()

    stop_words = set(stopwords.words('english'))
    tokens = [word for word in words if word not in stop_words]
    # Rejoin the cleaned words
    cleaned_abs = " ".join(tokens)
    return f"{year},{state},{cleaned_abs}"


# Define a function to check if a line matches the desired pattern
def is_valid_line(line):
    # Regex to match the format: year,state,text (with text having more than 20 characters)
    pattern = r"^\d{4},[A-Z]{2},.{20,}$"  # Year: 4 digits, State: 2 uppercase letters, Text: more than 20 characters
    return re.fullmatch(pattern, line)

# Open the file and process each line
def process_file(line):
    # Strip whitespace and newlines
    line = line.strip()

    # Validate the line
    if line and is_valid_line(line):
        return line
    return 0

def remove_punctuation(line):
    year = line[:4]
    state = line[5:7]
    abstract = line[8:]

    abstract = "".join(ch if ch.isalpha() else " " for ch in abstract)
    # abstract = re.sub(f"[{re.escape(string.punctuation)}]", " ", abstract)
    # abstract = " ".join(abstract.split())

    return f"{year},{state},{abstract}".strip()

def remove_single_letters(line):
    year = line[:4]
    state = line[5:7]
    abstract = line[8:]
    cleaned_abstract = " ".join(word for word in abstract.split() if len(word) != 1)
    return f"{year},{state},{cleaned_abstract}"

def lemmatization(line):
    year = line[:4]
    state = line[5:7]
    abstract = line[8:]
    lemmatizer = WordNetLemmatizer()
    lemmatized_abstract = " ".join([lemmatizer.lemmatize(word) for word in abstract.split()])
    return f"{year},{state},{lemmatized_abstract}"


def main():
    input_file = "./data/year_state_abs.csv"
    train_data = "./data/train_data.csv"
    validation_data = "./data/validation_data.csv"
    test_data = "./data/test_data.csv"

    train_file = open(train_data, "w")
    valid_file = open(validation_data, "w")
    test_file = open(test_data, "w")

    with open(input_file, "r") as file:
        lines = file.readlines()
    new_line_removed = remove_unwanted_newlines(lines)


    for line in new_line_removed:
        # for csv first line case
        if line == new_line_removed[0]:
            train_file.write(line + '\n')
            valid_file.write(line + '\n')
            test_file.write(line + '\n')
            continue
        # normalize formate to year,state,abstract
        line = process_file(line)
        # if line not in format year,state,abs remove it
        if line == 0: continue # continue to next line

        line = " ".join(line.split())

        # remove punctuation
        line = remove_punctuation(line)

        # turn to lowercase
        line = line.lower()

        line = remove_single_letters(line)

        # stemming or lemmatization
        line = lemmatization(line)

        # stopword removal
        line = rm_stop_words(line)

        seperator = random.random()
        if seperator < 0.8:
            train_file.write(line + '\n')
        elif 0.8 <= seperator < 0.9:
            valid_file.write(line + '\n')
        elif 0.9 <= seperator < 1:
            test_file.write(line + '\n')

    train_file.close()
    valid_file.close()
    test_file.close()

main()


# Example usage
# def main():
#     input_file = "/home/frankwoods/Desktop/lab/data/year_state_abs.csv"
#     output_file = "/home/frankwoods/Desktop/lab/data/test_output2.csv"

#     with open(input_file, "r") as file:
#         lines = file.readlines()
#     new_line_removed = remove_unwanted_newlines(lines)

#     cleaned_lines = []

#     for line in new_line_removed:
#         # for csv first line case
#         if line == new_line_removed[0]:
#             cleaned_lines.append(line)
#             continue
#         # normalize formate to year,state,abstract
#         line = process_file(line)
#         # if line not in format year,state,abs remove it
#         if line == 0: continue # continue to next line

#         line = " ".join(line.split())

#         # remove punctuation
#         line = remove_punctuation(line)

#         # turn to lowercase
#         line = line.lower()

#         line = remove_single_letters(line)

#         line = lemmatization(line)

#         # stopword removal
#         line = rm_stop_words(line)
#         # stemming or lemmatization



#         cleaned_lines.append(line + '\n')

#     with open(output_file, "w") as file:
#         file.writelines(cleaned_lines)

# main()

