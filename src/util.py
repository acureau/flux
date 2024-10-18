# Contains utility functions which may be used across the project.


import re


# Splits a name at whitespace, joins words with hyphens, standardizes case.
def name_to_path(name):
    return "-".join(re.sub(r"[^a-zA-Z0-9\s]", "", name).split()).lower()


# Writes text to a file.
def write_file_text(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


# Read text from a file.
def read_file_text(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
