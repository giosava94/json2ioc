import os
import json2ioc.paths as paths
from fixtures.conf import (
    conf_data,
    conf_dir,
    conf_dir_empty,
    conf_file,
    conf_file_not_json,
    empty_dir,
)
from fixtures.ioc import (
    ioc_dir_std,
    ioc_dir_std_with_conf_dir,
    ioc_dir_with_only_app,
    ioc_dir_with_only_iocboot,
    ioc_dir_std_with_subs_template,
    subs_template_txt,
)


def test_get_conf_files_with_empty_dir(conf_dir_empty):
    """
    Receives the empty directory `json_config`
    """
    path = conf_dir_empty.getpath("json_config")
    files = paths.get_conf_files(path)
    assert len(files) == 0


def test_get_conf_files_with_conf_dir(conf_dir):
    """
    Receives the directory `json_config` which has both
    json and not json files (in this case 1 json and 1 txt)
    """
    path = conf_dir.getpath("json_config")
    files = paths.get_conf_files(path)
    assert len(files) == 1


def test_get_conf_files_with_conf_file(conf_file):
    """
    Receives the name of a json file
    """
    files = paths.get_conf_files(conf_file)
    assert len(files) == 1


def test_get_conf_files_with_conf_file_not_json(conf_file_not_json):
    """
    Receives the name of a not json file
    """
    try:
        files = paths.get_conf_files(conf_file_not_json)
        assert 0
    except ValueError as e:
        assert str(e) == "'%s' is not a '.json' file" % conf_file_not_json


def test_get_conf_files_with_conf_file_not_existing():
    """
    Receives the name of a not existing file
    """
    try:
        files = paths.get_conf_files("not_existing.json")
        assert 0
    except FileNotFoundError as e:
        assert (
            str(e)
            == "'not_existing.json' not a valid path (neither a folder or a file)"
        )


def test_get_config_valid_path(conf_dir_empty):
    """
    Receives valid path. Workspace is ignored
    """
    conf_path = paths.get_config(conf_dir_empty.path)
    assert conf_path == conf_dir_empty.path
    conf_path = paths.get_config(conf_dir_empty.path, "invalid_workspace")
    assert conf_path == conf_dir_empty.path


def test_get_config_invalid_path():
    """
    Receives and invalid path.
    """
    try:
        conf_path = paths.get_config("invalid_path")
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Configuration file or directory 'invalid_path' not found"


def test_get_config_with_no_path(ioc_dir_std_with_conf_dir):
    """
    Receives None as conf_path.
    We execute the command from a valid path in order to get the correct workspace.
    """
    conf_path = paths.get_config(workspace=ioc_dir_std_with_conf_dir.path)
    assert conf_path == os.path.join(ioc_dir_std_with_conf_dir.path, "json_config")

    work_dir = os.getcwd()
    os.chdir(ioc_dir_std_with_conf_dir.path)
    conf_path = paths.get_config()
    os.chdir(work_dir)
    assert conf_path == os.path.join(".", "json_config")


def test_get_config_with_no_path_wrong_workspace():
    """
    Receives None as conf_path.
    The default folder in this case does not exists.
    We check in the raised error if the path concatenation is correct
    """
    try:
        conf_path = paths.get_config()
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Configuration file or directory './json_config' not found"

    workspace = "invalid_path"
    try:
        conf_path = paths.get_config(workspace=workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Received workspace '%s' not found" % workspace


def test_get_db_dir_valid_workspace(ioc_dir_std):
    """
    Receives a valid workspace.
    """
    db_dir = paths.get_db_dir(ioc_dir_std.path)
    assert db_dir == ioc_dir_std.getpath("testApp/Db")

    # TODO: Uncomment and test following lines
    # db_dir = paths.get_db_dir(ioc_dir_std.path, db="myDb")
    # assert db_dir == ioc_dir_std.getpath("testApp/Db")


def test_get_db_dir_invalid_workspace(empty_dir):
    """
    Receives invalid workspaces.
    - Not existing
    - Without *App folder
    - Without Db dir
    """
    workspace = "invalid_path"
    try:
        db_dir = paths.get_db_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Received workspace '%s' not found" % workspace

    workspace = empty_dir.path
    try:
        db_dir = paths.get_db_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert (
            str(e)
            == "Directory ending with 'App' in selected workspace '%s' not found"
            % workspace
        )


def test_get_db_dir_without_db_dir(ioc_dir_with_only_app):
    """
    Receives as workspace a an IOC with only the App folder
    """
    workspace = ioc_dir_with_only_app.path
    try:
        db_dir = paths.get_db_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Directory 'Db' inside '%s' not found" % os.path.join(
            workspace, "testApp"
        )


# TODO: Uncomment and test the following section
# def test_get_db_dir_without_specified_db_dir(ioc_dir_std, ioc_dir_with_only_app):
#    """
#    Specify the target Db folder.
#    Receives as workspace a an IOC with only the App folder
#    and a workspace without the specified db folder
#    """
#    workspace = ioc_dir_std.path
#    try:
#        db_dir = paths.get_db_dir(workspace, db="myDb")
#        assert 0
#    except FileNotFoundError as e:
#        assert str(e) == "Directory 'myDb' inside '%s' not found" % os.path.join(
#            workspace, "testApp"
#        )
#
#    workspace = ioc_dir_with_only_app.path
#    try:
#        db_dir = paths.get_db_dir(workspace, db="myDb")
#        assert 0
#    except FileNotFoundError as e:
#        assert str(e) == "Directory 'myDb' inside '%s' not found" % os.path.join(
#            workspace, "testApp"
#        )


def test_get_db_dir_with_no_path(ioc_dir_std_with_conf_dir):
    """
    Receives no arguments.
    We execute the command from a valid path in order to get the correct workspace.
    """
    db_dir = paths.get_db_dir(workspace=ioc_dir_std_with_conf_dir.path)
    assert db_dir == os.path.join(ioc_dir_std_with_conf_dir.path, "testApp/Db")

    work_dir = os.getcwd()
    os.chdir(ioc_dir_std_with_conf_dir.path)
    db_dir = paths.get_db_dir()
    os.chdir(work_dir)
    assert db_dir == os.path.join(".", "testApp/Db")


def test_get_makefile_valid_path(ioc_dir_std):
    """
    Receives a valid path.
    """
    path = ioc_dir_std.getpath("testApp/Db")
    makefile = paths.get_makefile(path)
    assert makefile == os.path.join(path, "Makefile")


def test_get_makefile_invalid_path():
    """
    Receives an invalid path or a path not containing a make file.
    """
    try:
        makefile = paths.get_makefile("invalid_path")
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "'invalid_path/Makefile' not found"


def test_get_st_cmd_dir_valid_workspace(ioc_dir_std):
    """
    Receives a valid workspace.
    """
    st_cmd_dir = paths.get_st_cmd_dir(ioc_dir_std.path)
    assert st_cmd_dir == os.path.join(ioc_dir_std.path, "iocBoot/ioctest")

    work_dir = os.getcwd()
    os.chdir(ioc_dir_std.path)
    st_cmd_dir = paths.get_st_cmd_dir()
    os.chdir(work_dir)
    assert st_cmd_dir == os.path.join(".", "iocBoot/ioctest")


def test_get_st_cmd_dir_invalid_workspace(empty_dir, ioc_dir_with_only_iocboot):
    """
    Receives invalid workspaces.
    """
    workspace = "invalid_path"
    try:
        st_cmd_dir = paths.get_st_cmd_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Received workspace '%s' not found" % workspace

    workspace = empty_dir.path
    try:
        st_cmd_dir = paths.get_st_cmd_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert (
            str(e)
            == "Directory 'iocBoot' in selected workspace '%s' not found" % workspace
        )

    workspace = ioc_dir_with_only_iocboot.path
    try:
        st_cmd_dir = paths.get_st_cmd_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(
            e
        ) == "Folder starting with 'ioc' inside '%s' not found" % os.path.join(
            workspace, "iocBoot"
        )


def test_get_st_cmd_out_dir_valid_path(empty_dir):
    """
    Receives valid path. Workspace is ignored
    """
    out_dir = paths.get_st_cmd_out_dir(empty_dir.path)
    assert out_dir == empty_dir.path
    out_dir = paths.get_st_cmd_out_dir(empty_dir.path, "invalid_workspace")
    assert out_dir == empty_dir.path


def test_get_st_cmd_out_dir_invalid_path():
    """
    Receives and invalid path.
    """
    out_dir = "invalid_path"
    try:
        out_dir = paths.get_st_cmd_out_dir(out_dir)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Output directory for start command 'invalid_path' not found"


def test_get_st_cmd_out_dir_no_path(ioc_dir_std):
    """
    Receives None as out_dir but the workspace is valid
    """
    out_dir = paths.get_st_cmd_out_dir(workspace=ioc_dir_std.path)
    assert out_dir == ioc_dir_std.getpath("iocBoot/ioctest")

    work_dir = os.getcwd()
    os.chdir(ioc_dir_std.path)
    out_dir = paths.get_st_cmd_out_dir()
    os.chdir(work_dir)
    assert out_dir == os.path.join(".", "iocBoot/ioctest")


def test_get_st_cmd_template_valid_path(ioc_dir_std):
    """
    Receives valid path. Workspace is ignored
    """
    path = ioc_dir_std.getpath("iocBoot/ioctest/st.cmd")
    st_cmd = paths.get_st_cmd_template(path)
    assert st_cmd == path
    st_cmd = paths.get_st_cmd_template(path, "invalid_workspace")
    assert st_cmd == path


def test_get_st_cmd_template_invalid_path(ioc_dir_std):
    """
    Receives an invalid path.
    """
    path = "invalid_path"
    try:
        st_cmd = paths.get_st_cmd_template(path)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Substitutions file '%s' not found" % path


def test_get_st_cmd_template_no_path(ioc_dir_std):
    """
    Receives None as st_cmd but the workspace is valid
    """
    st_cmd = paths.get_st_cmd_template(workspace=ioc_dir_std.path)
    assert st_cmd == os.path.join(ioc_dir_std.path, "iocBoot/ioctest/st.cmd")

    work_dir = os.getcwd()
    os.chdir(ioc_dir_std.path)
    st_cmd = paths.get_st_cmd_template()
    os.chdir(work_dir)
    assert st_cmd == os.path.join(".", "iocBoot/ioctest/st.cmd")


def test_get_subs_out_dir_valid_path(empty_dir):
    """
    Receives valid path. Workspace is ignored
    """
    out_dir = paths.get_subs_out_dir(empty_dir.path)
    assert out_dir == empty_dir.path
    out_dir = paths.get_subs_out_dir(empty_dir.path, "invalid_workspace")
    assert out_dir == empty_dir.path


def test_get_subs_out_dir_invalid_path():
    """
    Receives and invalid path.
    """
    out_dir = "invalid_path"
    try:
        out_dir = paths.get_subs_out_dir(out_dir)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Output directory for substitutions 'invalid_path' not found"


def test_get_subs_out_dir_no_path(ioc_dir_std):
    """
    Receives None as out_dir but the workspace is valid
    """
    out_dir = paths.get_subs_out_dir(workspace=ioc_dir_std.path)
    assert out_dir == ioc_dir_std.getpath("testApp/Db")

    work_dir = os.getcwd()
    os.chdir(ioc_dir_std.path)
    out_dir = paths.get_subs_out_dir()
    os.chdir(work_dir)
    assert out_dir == os.path.join(".", "testApp/Db")


def test_set_subs_template_valid_path(ioc_dir_std_with_subs_template):
    """
    Receives valid path. Workspace is ignored
    """
    path = ioc_dir_std_with_subs_template.getpath("testApp/Db/template.substitutions")
    template = paths.get_subs_template(path)
    assert template == path
    template = paths.get_subs_template(path, "invalid_workspace")
    assert template == path


def test_set_subs_template_invalid_path(ioc_dir_std_with_subs_template):
    """
    Receives an invalid path.
    """
    path = "invalid_path"
    try:
        template = paths.get_subs_template(path)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Substitutions file '%s' not found" % path


def test_set_subs_template_no_path(ioc_dir_std_with_subs_template):
    """
    Receives None as template but the workspace is valid
    """
    template = paths.get_subs_template(workspace=ioc_dir_std_with_subs_template.path)
    assert template == os.path.join(
        ioc_dir_std_with_subs_template.path, "testApp/Db/template.substitutions"
    )

    work_dir = os.getcwd()
    os.chdir(ioc_dir_std_with_subs_template.path)
    template = paths.get_subs_template()
    os.chdir(work_dir)
    assert template == os.path.join(".", "testApp/Db/template.substitutions")


def test_check_workspace_valid():
    """
    Receive an existing folder
    """
    workspace = "."
    path = paths.check_workspace(".")
    assert path == "."


def test_check_workspace_file(conf_file):
    """
    Receive an axisting file but not a dir
    """
    workspace = conf_file
    try:
        path = paths.check_workspace(conf_file)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Received workspace '%s' not found" % workspace


def test_check_workspace_not_existing():
    """
    Receive a non existing path
    """
    workspace = "invalid_path"
    try:
        path = paths.check_workspace(workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Received workspace '%s' not found" % workspace
