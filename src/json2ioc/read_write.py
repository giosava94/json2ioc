import json


def load_data_from_json(name):
    """
    Load dictionary with json.
    """

    with open(name, "r") as f:
        data = json.load(f)
    return data


def load_text_from_file(name):
    """
    Loading text.
    """

    with open(name, "r") as f:
        text = f.read()
    return text


def load_lines_from_file(name):
    """
    Load lines.
    """

    with open(name, "r") as f:
        lines = f.readlines()
    return lines


def write_text_to_file(name, text):
    """
    Write to file.
    """

    with open(name, "w") as f:
        f.write(text)


def write_lines_to_file(name, lines):
    """
    Write lines to file.
    """

    if not type(lines) is list:
        raise TypeError("Received lines value '%s' is not a list" % lines)
    with open(name, "w") as f:
        f.writelines(lines)
