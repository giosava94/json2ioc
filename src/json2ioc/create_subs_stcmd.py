#!/usr/bin/env python3

import json, os, re
from .parser import parser
from .paths import (
    get_config,
    get_conf_files,
    get_makefile,
    get_st_cmd_template,
    get_subs_out_dir,
    get_subs_template,
    get_work_dir,
)


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

    with open(name, "w") as f:
        f.writelines(lines)


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


def generate_substitutions(inp_text, conf):
    """
    From configuration file and input text,
    search the `{pattern {` string and then
    substitute macros and create substitutions file.
    """

    out_text = ""
    start_idx = 0
    target = re.compile(r"\{[\s]*pattern[\s]*\{[^\{]*", re.DOTALL)

    if target is None:
        raise Exception("Valid '{ pattern {' expression not found")

    while True:
        m = re.search(target, inp_text[start_idx:])
        if m is None:
            break
        out_text, end_idx = replace_text(inp_text[start_idx:], conf, m.end(), out_text)
        start_idx += end_idx

    return out_text


def add_subs_to_makefile(lines, subs_list):
    """
    Add to makefile new substitutions files
    """

    new_lines = lines[:]
    i = 0
    for l, line in enumerate(new_lines):
        if "DB +=" in line:
            i = l
    for sub in subs_list:
        new_line = "DB += %s\n" % sub
        if not new_line in new_lines:
            new_lines.insert(i + 1, new_line)
            i += 1
    return new_lines


def create_start_command(st_cmd, subs_list, st_cmd_folder):
    with open(st_cmd, "r") as f:
        lines = f.readlines()

    db_load_template_comment_line = 0
    env_paths_comment_line = 0
    for l, line in enumerate(lines):
        if "#< envPaths" in line:
            env_paths_comment_line = l
        if "## Load record instances" in line:
            db_load_template_comment_line = l

    for sub in subs_list:
        out_lines = lines[:]
        name = st_cmd_folder + sub[:-14] + ".cmd"
        out_lines[env_paths_comment_line] = out_lines[env_paths_comment_line][1:]
        out_lines[db_load_template_comment_line + 1] = (
            "#" + out_lines[db_load_template_comment_line + 1]
        )
        out_lines.insert(
            db_load_template_comment_line + 2,
            'dbLoadTemplate("../../db/' + sub + '")\n',
        )
        with open(name, "w") as f:
            f.writelines(out_lines)
        print("Create '%s'" % name)


def main():
    args = vars(parser())

    # Get correct inputs and outputs.
    # Check file and folder existence
    workspace = get_work_dir(args.get("workspace"))
    config_path = get_config(args.get("config"), workspace)
    subs_template = get_subs_template(args.get("subs_template"), workspace)
    st_cmd = get_st_cmd_template(args.get("st_cmd_template"), workspace)
    subs_out = get_subs_out_dir(args.get("subs_out"), workspace)
    run_make = args.get("make", False)

    conf_files = get_conf_files(config_path)
    if len(conf_files) == 0:
        print("No configuration files")
        return
    subs_text = load_text_from_file(subs_template)

    # Create substitutions
    subs_list = []
    for conf in conf_files:
        config = load_data_from_json(conf)
        out_text = generate_substitutions(subs_text, config)
        file_name = os.path.basename(conf)[:-5] + ".substitutions"
        dest_name = subs_out + file_name
        write_text_to_file(dest_name, out_text)
        subs_list.append(file_name)
        print("Created '%s'" % dest_name)

    print("")

    # Update Makefile
    makefile = get_makefile(subs_out)
    makefile_lines = load_lines_from_file(makefile)
    lines = add_subs_to_makefile(makefile_lines, subs_list)
    write_lines_to_file(makefile, lines)
    print("Updated %s" % makefile)

    print("")

    # Create start command
    create_start_command(st_cmd, subs_list, st_cmd_folder)

    print("\nProcedure complete.")

    if not run_make:
        make = input("Do you want to compile? [y/N] ")
    if run_make or make.lower() == "y":
        print("Compiling\n")
        os.system("make -j $(nproc)")
        print("\nProject compiled")


if __name__ == "__main__":
    main()