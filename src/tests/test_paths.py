import pytest, os
import json2ioc.paths as paths
from fixtures.paths import (
    json_empty_conf_dir,
    json_conf_dir,
    json_conf_json_file,
    json_conf_not_json_file,
    empty_dir,
    ioc_dir,
    ioc_dir_with_only_app,
    ioc_dir_with_only_iocboot,
)


def test_get_conf_files(
    json_empty_conf_dir,
    json_conf_dir,
    json_conf_json_file,
    json_conf_not_json_file,
):
    """
    Test `get_conf_files`
    """

    # Receives the empty directory `json_config`
    path = json_empty_conf_dir.getpath("json_config")
    files = paths.get_conf_files(path)
    assert len(files) == 0

    # Receives the directory `json_config` which has both
    # json and not json files (in this case 1 json and 1 txt)
    path = json_conf_dir.getpath("json_config")
    files = paths.get_conf_files(path)
    assert len(files) == 1

    # Receives the name of a json file
    files = paths.get_conf_files(json_conf_json_file)
    assert len(files) == 1

    # Receives the name of a not json file
    try:
        files = paths.get_conf_files(json_conf_not_json_file)
        assert 0
    except ValueError:
        assert 1

    # Receives the name of a not existing file
    try:
        files = paths.get_conf_files("not_existing.json")
        assert 0
    except FileNotFoundError:
        assert 1


def test_get_config(json_empty_conf_dir):
    """
    Test `get_config`
    """

    # Receives valid path. Workspace is ignored
    conf_path = paths.get_config(json_empty_conf_dir.path)
    assert conf_path == json_empty_conf_dir.path
    conf_path = paths.get_config(json_empty_conf_dir.path, ".")
    assert conf_path == json_empty_conf_dir.path

    # Receives and invalid path.
    try:
        conf_path = paths.get_config("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1

    # Receives None as conf_path.
    # The default folder in this case does not exists.
    # We check in the raised error if the path concatenation is correct
    try:
        conf_path = paths.get_config()
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Configuration file or directory './json_config/' not found"
    try:
        conf_path = paths.get_config(workspace="workspace")
        assert 0
    except FileNotFoundError as e:
        assert (
            str(e)
            == "Configuration file or directory 'workspace/json_config/' not found"
        )


def test_get_db_dir(empty_dir, ioc_dir_with_only_app, ioc_dir):
    """
    Test `get_db_dir`
    """

    # Receives a valid workspace.
    db_dir = paths.get_db_dir(ioc_dir.path)
    assert db_dir == os.path.join(ioc_dir.path, "testApp/Db/")

    # Receives an invalid workspaces.
    workspace = "invalid_path"
    try:
        db_dir = paths.get_db_dir(workspace)
        assert 0
    except FileNotFoundError:
        assert 1
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
    workspace = ioc_dir_with_only_app.path
    try:
        db_dir = paths.get_db_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(e) == "Directory 'Db/' inside '%s' not found" % os.path.join(
            workspace, "testApp"
        )


def test_get_makefile(ioc_dir):
    """
    Test `get_makefile`
    """

    # Receives a valid path.
    path = ioc_dir.getpath("testApp/Db")
    makefile = paths.get_makefile(path)
    assert makefile == os.path.join(path, "Makefile")

    # Receives an invalid path or a path not containing a make file.
    try:
        makefile = paths.get_makefile("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1
    try:
        makefile = paths.get_makefile("testApp")
        assert 0
    except FileNotFoundError:
        assert 1


def test_get_st_cmd_dir(empty_dir, ioc_dir_with_only_iocboot, ioc_dir):
    """
    Test `get_st_cmd_dir`
    """

    # Receives a valid workspace.
    db_dir = paths.get_st_cmd_dir(ioc_dir.path)
    assert db_dir == os.path.join(ioc_dir.path, "iocBoot/ioctest")

    # Receives an invalid workspaces.
    workspace = "invalid_path"
    try:
        db_dir = paths.get_st_cmd_dir(workspace)
        assert 0
    except FileNotFoundError:
        assert 1
    workspace = empty_dir.path
    try:
        db_dir = paths.get_st_cmd_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert (
            str(e)
            == "Directory 'iocBoot' in selected workspace '%s' not found" % workspace
        )
    workspace = ioc_dir_with_only_iocboot.path
    try:
        db_dir = paths.get_st_cmd_dir(workspace)
        assert 0
    except FileNotFoundError as e:
        assert str(
            e
        ) == "Folder starting with 'ioc' inside '%s' not found" % os.path.join(
            workspace, "iocBoot"
        )


def test_get_st_cmd_out_dir(ioc_dir):
    """
    Test `get_st_cmd_out_dir`
    """

    # Receives valid path. Workspace is ignored
    out_dir = paths.get_st_cmd_out_dir(ioc_dir.path)
    assert out_dir == ioc_dir.path
    out_dir = paths.get_st_cmd_out_dir(ioc_dir.path, ".")
    assert out_dir == ioc_dir.path

    # Receives and invalid path.
    try:
        out_dir = paths.get_st_cmd_out_dir("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1

    # Receives None as out_dir but the workspace is valid
    out_dir = paths.get_st_cmd_out_dir(workspace=ioc_dir.path)
    assert out_dir == ioc_dir.getpath("iocBoot/ioctest")

    # Receives None as out_dir but the workspace is not valid
    # (The test workspace is invalid)
    try:
        out_dir = paths.get_st_cmd_out_dir()
        assert 0
    except FileNotFoundError:
        assert 1


def test_get_st_cmd_template(ioc_dir):
    """
    Test `get_st_cmd_template`
    """

    # Receives valid path. Workspace is ignored
    path = ioc_dir.getpath("iocBoot/ioctest/st.cmd")
    st_cmd = paths.get_st_cmd_template(path)
    assert st_cmd == path
    st_cmd = paths.get_st_cmd_template(path, "workspace")
    assert st_cmd == path

    # Receives and invalid path.
    try:
        st_cmd = paths.get_st_cmd_template("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1

    # Receives None as st_cmd but the workspace is valid
    st_cmd = paths.get_st_cmd_template(workspace=ioc_dir.path)
    assert st_cmd == path

    # Receives None as out_dir but the workspace is not valid
    # (The test workspace is invalid)
    try:
        st_cmd = paths.get_st_cmd_template()
        assert 0
    except FileNotFoundError:
        assert 1