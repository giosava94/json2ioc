import os


def get_conf_files(config):
    conf_files = []
    if os.path.isdir(config):
        for f in os.listdir(config):
            if ".json" in f:
                conf_files.append(config + f)
    elif os.path.isfile(config):
        if config.endswith(".json"):
            conf_files.append(config)
        else:
            raise ValueError("'%s' is not a '.json' file" % config)
    else:
        raise FileNotFoundError(
            "'%s' not a valid path (neither a folder or a file)" % config
        )
    return conf_files


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


def get_makefile(subs_out):
    """
    Load from the substitutions destination folder the makefile.
    Raise error if the *App/Db/Makefile is not a file.
    """

    makefile = subs_out + "Makefile"
    if os.path.isfile(makefile):
        return makefile
    raise FileNotFoundError("'%s' not found" % makefile)


def get_st_cmd_dir(workspace):
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
        db_dir = get_st_cmd_dir(workspace)
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


def get_work_dir(workspace):
    """
    Correctly format received workspace dir.
    Raise error if the workspace does not exist.
    """

    workspace += "" if workspace[-1] == "/" else "/"
    if os.path.isdir(workspace):
        return workspace
    raise FileNotFoundError("Received workspace '%s' not found" % workspace)
