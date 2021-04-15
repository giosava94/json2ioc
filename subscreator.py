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

    dest_name = out_path + os.path.basename(conf).strip(".json") + ".substitutions"
    create_substitutions_file(out_text, dest_name)
    return os.path.basename(conf).strip(".json") + ".substitutions"


def add_subs_to_makefile(makefile, subs_list):
    """
    Add to makefile new substitutions files
    """

    with open(makefile, "r") as f:
        lines = f.readlines()
    i = 0
    for l, line in enumerate(lines):
        if "DB +=" in line:
            i = l
    for sub in subs_list:
        new_line = "DB += %s\n" % sub
        if not new_line in lines:
            lines.insert(i + 1, new_line)
            i += 1
    with open(makefile, "w") as f:
        f.writelines(lines)
    print("Makefile updated")


if __name__ == "__main__":
    args = vars(parser())

    for f in os.listdir():
        if "App" in f:
            app_path = f + "/"

    # Configuration folder and files definition
    if args["config"] is None:
        conf_path = app_path + "config/"
    else:
        conf_path = args["config"]
        conf_path += "" if conf_path[-1] == "/" else "/"
    conf_files = []
    if os.path.isdir(conf_path):
        for f in os.listdir(conf_path):
            if ".json" in f:
                conf_files.append(conf_path + f)
    else:
        print(
            """'%s' folder does not exist. Create it 
            and add there your configuration files 
            (.json files) and the template.substitutions."""
            % conf_path
        )
        exit()

    # Template file definition
    template = args["template"]
    if os.path.isfile(conf_path + template):
        inp_text = load_template_from_file(conf_path + template)
    else:
        print("Template file '%s' does not exist" % conf_path + template)
        exit()

    # Output path existence check
    if args["out"] is None:
        out_path = app_path + "Db/"
    else:
        out_path = args["out"]
        out_path += "" if out_path[-1] == "/" else "/"
    if not os.path.isdir(out_path):
        print("Output folder '%s' does not exist." % out_path)
        exit()

    # Create substitutions
    subs_list = []
    for conf in conf_files:
        subs_list.append(substitute(conf, inp_text, out_path))

    # Update Makefile
    makefile = out_path + "Makefile"
    add_subs_to_makefile(makefile, subs_list)