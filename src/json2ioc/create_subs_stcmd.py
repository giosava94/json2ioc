#!/usr/bin/env python3

import json, os, re
from .parser import parser


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


def create_file(name, text):
    """
    Create file
    """

    print("Create '%s'" % name)
    with open(name, "w") as f:
        f.write(text)


def create_substitutions(conf, inp_text, out_path):
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

    dest_name = out_path + os.path.basename(conf)[:-5] + ".substitutions"
    create_file(dest_name, out_text)
    return dest_name


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


def get_db_dir(workspace, db="Db/"):
    """
    Check if workspace dir contains a *App folder
    with the given Db directory and return it.
    Return error if the App dir does not exist.
    Raise error if *App or the given db folder do not exist.
    """

    for f in os.listdir(workspace):
        if f.endswith("App"):
            app_dir = workspace + f + "/"
            db_dir = app_dir + db
            db_dir += "" if db_dir[-1] == "/" else "/"
            if os.path.isdir(db_dir):
                return db_dir
            raise FileNotFoundError(
                "Directory '%s' inside '%s' not found" % (db, app_dir)
            )
    raise FileNotFoundError(
        "Directory ending with 'App' in selected workspace '%s' not found" % workspace
    )


def get_work_dir(workspace):
    """
    Correctly format received workspace dir.
    Raise error if the workspace does not exist.
    """

    workspace += "" if workspace[-1] == "/" else "/"
    if os.path.isdir(workspace):
        return workspace
    raise FileNotFoundError("Received workspace '%s' not found" % workspace)


def get_config(conf_path, workspace):
    """
    Set the correct path to the configuration folder
    or file based on the chosen workspace.
    Return the path to the json configuration file or dir.
    Raise error if the the given path is not valid.
    """

    if conf_path is None:
        conf_path = workspace + "json_config/"
    if os.path.exists(conf_path):
        return conf_path
    raise FileNotFoundError(
        "Configuration file or directory '%s' not found" % conf_path
    )


def get_subs_template(subs_template, workspace):
    """
    Return the default substitutions template if no one is given.
    In any case raise error if the template does not exists.
    """

    if subs_template is None:
        db_dir = get_db_dir(workspace)
        subs_template = db_dir + "template.substitutions"
    if os.path.isfile(subs_template):
        return subs_template
    raise FileNotFoundError("Substitutions file '%s' not found" % subs_template)


def st_cmd_dir(workspace):
    """
    Check if workspace dir contains an iocBoot folder
    with and ioc* folder inside and return it.
    Raise an error if one of the parent folder do not exist.
    """

    for f in os.listdir(workspace):
        if f == "iocBoot":
            ioc_boot_dir = workspace + f + "/"
            for d in os.listdir(ioc_boot_dir):
                if d.startswith("ioc"):
                    st_cmd_dir = ioc_boot_dir + d + "/"
                    return st_cmd_dir
            raise FileNotFoundError(
                "Folder starting with 'ioc' inside '%s' not found" % (ioc_boot_dir)
            )
    raise FileNotFoundError(
        "Directory 'iocBoot' in selected workspace '%s' not found" % workspace
    )


def get_st_cmd_template(st_cmd_template, workspace):
    """
    Return the start command created when generating the IOC
    with makeBaseApp.pl if no start command is specified.
    In any case raise error if the start command does not exist.
    """

    if st_cmd_template is None:
        db_dir = st_cmd_dir(workspace)
        st_cmd_template = db_dir + "st.cmd"
    if os.path.isfile(st_cmd_template):
        return st_cmd_template
    raise FileNotFoundError("Substitutions file '%s' not found" % st_cmd_template)


def get_subs_out_dir(subs_out, workspace):
    """
    Return the correct output folder for the substitutions files.
    By default it is the *App/Db one if it exists.
    Raise error if the specified folder does not exist.
    """

    if subs_out is None:
        return get_db_dir(workspace)
    elif os.path.isdir(subs_out):
        subs_out += "" if subs_out[-1] == "/" else "/"
        return subs_out
    raise FileNotFoundError(
        "Output directory for substitutions '%s' not found" % subs_out
    )


def main():
    args = vars(parser())

    # Get correct inputs and outputs.
    # Check file and folder existence
    workspace = get_work_dir(args.get("workspace"))
    config = get_config(args.get("config"), workspace)
    subs_template = get_subs_template(args.get("subs_template"), workspace)
    st_cmd = get_st_cmd_template(args.get("st_cmd_template"), workspace)
    subs_out = get_subs_out_dir(args.get("subs_out"), workspace)
    run_make = args.get("make", False)

    # Configuration folder and files definition
    conf_files = []
    if os.path.isdir(conf_path):
        for f in os.listdir(conf_path):
            if ".json" in f:
                conf_files.append(conf_path + f)
    else:
        print(
            "'%s' folder does not exist. Create it and add there your configuration files (.json files) and the template.substitutions."
            % conf_path
        )
        exit()

    # Template file definition
    template = args.get("template", None)
    if os.path.isfile(conf_path + template):
        subs_text = load_template_from_file(conf_path + template)
    else:
        print("Template file '%s' does not exist" % conf_path + template)
        exit()

    # Create substitutions
    subs_list = []
    for conf in conf_files:
        name = create_substitutions(conf, subs_text, out_path)
        subs_list.append(os.path.basename(name))

    print("")

    # Update Makefile
    makefile = out_path + "Makefile"
    add_subs_to_makefile(makefile, subs_list)

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