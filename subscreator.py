import json, os, re
from parse import parser


def load_config_from_file(name):
    """
    Load configuration file.
    """

    print("Load configuration file: %s" % name)
    with open(name, "r") as f:
        config = json.load(f)
    return config


def load_template_from_file(name):
    """
    Loading template file.
    """

    print("Load template file: %s" % name)
    with open(name, "r") as f:
        text = f.read()
    return text


def replace_text(inp_text, config, start=0, out_text=""):
    """
    Given an input text, and a configuration object,
    starting from the given index replace
    all the macros defined in the configuration.
    Append the result to the given output text string.
    Return the output text and the index of the last char,
    of the input text, taken into accout for the replacement.
    """

    inp_lines, end_idx = find_lines_to_replace(inp_text, start)
    restrict_text = inp_text[:end_idx]

    out_lines = []
    for item in config.values():
        out_lines += replace_macros(inp_lines, item)

    old_string = "".join(inp_lines)
    new_string = "".join(out_lines)
    out_text += restrict_text.replace(old_string, new_string, 1)

    return out_text, end_idx


def find_lines_to_replace(inp_text, start=0):
    """
    In the given input text, starting from the given start index,
    find all blocks of code, splitting them into lines,
    where the replace action must take place.
    Return the lines to replace and the last index
    of the text block to replace.
    """

    inp_lines = []
    end = start
    counter = 0
    while True:
        if inp_text[end] == "{":
            counter += 1
        elif inp_text[end] == "}":
            counter -= 1
            if counter == -1:
                break
        elif inp_text[end] == "\n":
            inp_lines.append(inp_text[start : end + 1])
            start = end + 1
        end += 1
    return inp_lines, end + 1


def replace_macros(inp_lines, item):
    """
    For each line find the macro and replace it with the correct value.
    Return the updated lines.
    """

    new_lines = inp_lines[:]
    for k, v in item.items():
        for i in range(len(inp_lines)):
            new_lines[i] = new_lines[i].replace("$(%s)" % k, v)
    return new_lines


def create_substitutions_file(text, name):
    """
    Create substitutions file
    """

    print("Create substitutions: %s" % name)
    with open(name, "w") as f:
        f.write(text)


def substitute(conf, inp_text, out_path):
    """
    From configuration file and input text,
    search the `{pattern {` string and then
    substitute macros and create substitutions file.
    """

    out_text = ""
    start_idx = 0
    target = re.compile(r"\{[\s]*pattern[\s]*\{[^\{]*", re.DOTALL)
    config = load_config_from_file(conf)

    while True:
        m = re.search(target, inp_text[start_idx:])
        if m is None:
            break
        out_text, end_idx = replace_text(
            inp_text[start_idx:], config, m.end(), out_text
        )
        start_idx += end_idx

    det_name = out_path + "/" + os.path.basename(conf).strip(".json") + ".substitutions"
    create_substitutions_file(out_text, det_name)


if __name__ == "__main__":
    args = vars(parser())

    conf = args["config"]

    template = args["template"]
    if os.path.isfile(template):
        inp_text = load_template_from_file(template)
    else:
        print("Template file '%s' does not exist" % template)
        exit()

    if args["out"] == None:
        out_path = os.path.dirname(template)
        if out_path == "":
            out_path = "."
    else:
        out_path = args["out"]

    if os.path.isdir(conf):
        for f in os.listdir(conf):
            if ".json" in f:
                substitute(conf + "/" + f, inp_text, out_path)
    elif os.path.isfile(conf):
        substitute(conf, inp_text, out_path)
    else:
        print("Configuration file/path '%s' does not exist" % conf)
        exit()