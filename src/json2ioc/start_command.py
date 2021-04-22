def get_st_cmd_relevant_indices(lines):
    """
    Parse the start command lines and find the lines with relevant comments
    - < envPaths -> It must be de-commented
    - Load record instances -> Next line will be commented then the app will load users substitutions
    Return a dict with the corresponding indices
    """

    if not type(lines) is list:
        raise TypeError("'lines' expects a list. Found type is '%s'" % type(lines))

    db_load_template_comment_line = 0
    env_paths_comment_line = 0
    for l, line in enumerate(lines):
        if "< envPaths" in line:
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
    - < envPaths -> It must be de-commented
    - Load record instances -> Next line will be commented then the app will load users substitutions
    """

    if not type(lines) is list:
        raise TypeError("'lines' expects a list. Found type is '%s'" % type(lines))
    if not type(indices) is dict:
        raise TypeError("'indices' expects a dict. Found type is '%s'" % type(indices))
    if not type(subs) is str:
        raise TypeError("'subs' expects a str. Found type is '%s'" % type(subs))

    epcl = indices.get("env_paths_comment_line", -1)
    dltcl = indices.get("db_load_template_comment_line", -1)
    out_lines = lines[:]
    if epcl >= 0:
        out_lines[epcl] = "< envPaths"
    if dltcl >= 0:
        out_lines[dltcl + 1] = "#" + out_lines[dltcl + 1]
        out_lines.insert(dltcl + 2, 'dbLoadTemplate("../../db/' + subs + '")\n')
    return out_lines
