#!/usr/bin/env python3

import os
from .parser import parser
from .substitutions import generate_substitutions, add_subs_to_makefile
from .start_command import get_st_cmd_relevant_indices, generate_start_command
from .paths import (
    get_config,
    get_conf_files,
    get_makefile,
    get_st_cmd_dir,
    get_st_cmd_template,
    get_subs_out_dir,
    get_subs_template,
    get_work_dir,
)
from .read_write import (
    load_data_from_json,
    load_lines_from_file,
    load_text_from_file,
    write_lines_to_file,
    write_text_to_file,
)

def main():
    args = vars(parser())

    # Get correct inputs and outputs from args.
    # Check file and folder existence
    workspace = get_work_dir(args.get("workspace"))
    config_path = get_config(args.get("config"), workspace)
    subs_template = get_subs_template(args.get("subs_template"), workspace)
    st_cmd = get_st_cmd_template(args.get("st_cmd_template"), workspace)
    subs_out = get_subs_out_dir(args.get("subs_out"), workspace)
    run_make = args.get("make")

    conf_files = get_conf_files(config_path)
    if len(conf_files) == 0:
        print("No configuration files")
        exit()
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

    # Update Makefile
    makefile = get_makefile(subs_out)
    makefile_lines = load_lines_from_file(makefile)
    lines = add_subs_to_makefile(makefile_lines, subs_list)
    write_lines_to_file(makefile, lines)
    print("\nUpdated %s\n" % makefile)

    # Compilation
    if run_make:
        os.system("make -j $(nproc)")
        print("\nProject compiled\n")
    else:
        print("Skipping compilation\n")

    # Create start command
    st_cmd_dir = get_st_cmd_dir(workspace)
    st_cmd_lines = load_lines_from_file(st_cmd)
    indices = get_st_cmd_relevant_indices(st_cmd_lines)
    for substitution in subs_list:
        new_lines = generate_start_command(st_cmd_lines, indices, substitution)
        file_name = os.path.basename(substitution)[:-14] + ".cmd"
        dest_name = st_cmd_dir + file_name
        write_lines_to_file(dest_name, new_lines)
        print("Create '%s'" % dest_name)

    print("\nProcedure complete.")

if __name__ == "__main__":
    main()