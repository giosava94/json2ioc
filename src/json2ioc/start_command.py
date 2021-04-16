def get_st_cmd_relevant_indices(lines):
    """
    Parse the start command lines and find the lines with relevant comments
    - #< envPaths -> It must be de-commented
    - # Load record instances -> Next line will be commented then the app will load users substitutions
    Return a dict with the corresponding indices
    """

    db_load_template_comment_line = 0
    env_paths_comment_line = 0
    for l, line in enumerate(lines):
        if "#< envPaths" in line:
            env_paths_comment_line = l
        if "## Load record instances" in line:
            db_load_template_comment_line = l
    return {
        "db_load_template_comment_line": db_load_template_comment_line,
        "env_paths_comment_line": env_paths_comment_line,
    }


def generate_start_command(lines, indices, subs):
    """
    Generate new start command lines editing existing ones and adding new ones.
    - #< envPaths -> It must be de-commented
    - # Load record instances -> Next line will be commented then the app will load users substitutions
    """

    epcl = indices["env_paths_comment_line"]
    dltcl = indices["db_load_template_comment_line"]
    out_lines = lines[:]
    out_lines[epcl] = out_lines[epcl][1:]
    out_lines[dltcl + 1] = "#" + out_lines[dltcl + 1]
    out_lines.insert(dltcl + 2, 'dbLoadTemplate("../../db/' + subs + '")\n')
    return out_lines
