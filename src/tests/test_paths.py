import pytest, os
import json2ioc.paths as paths
from fixtures.paths import (
    empty_dir,
    ioc_dir,
    ioc_dir_with_only_app,
    json_empty_conf_dir,
    json_conf_dir,
    json_conf_json_file,
    json_conf_not_json_file,
)


"""
GET_CONF_FILES
"""


def test_get_conf_files_dir_len0(json_empty_conf_dir):
    """
    `gwt_conf_files` receives the empty directory `json_config`
    """
    files = paths.get_conf_files(os.path.join(json_empty_conf_dir.path, "json_config"))
    assert len(files) == 0


def test_get_conf_files_dir_len1(json_conf_dir):
    """
    `gwt_conf_files` receives the directory `json_config`
    which has both json and not json files (in this case
    1 json and 1 txt)
    """
    files = paths.get_conf_files(os.path.join(json_conf_dir.path, "json_config"))
    assert len(files) == 1


def test_get_conf_files_json_file(json_conf_json_file):
    """
    `gwt_conf_files` receives the name of a json file
    """
    files = paths.get_conf_files(json_conf_json_file)
    assert len(files) == 1


def test_get_conf_files_not_json_file(json_conf_not_json_file):
    """
    `gwt_conf_files` receives the name of a not json file
    """
    try:
        files = paths.get_conf_files(json_conf_not_json_file)
        assert 0
    except ValueError:
        assert 1


def test_get_conf_files_not_exist_file():
    """
    `gwt_conf_files` receives the name of a not existing file
    """
    try:
        files = paths.get_conf_files("not_existing.json")
        assert 0
    except FileNotFoundError:
        assert 1


"""
GET CONFIG
"""


def test_get_config(json_empty_conf_dir):
    """
    `get_config` receives valid path. Workspace is ignored
    """
    conf_path = paths.get_config(json_empty_conf_dir.path)
    assert conf_path == json_empty_conf_dir.path
    conf_path = paths.get_config(json_empty_conf_dir.path, ".")
    assert conf_path == json_empty_conf_dir.path


def test_get_config_without_conf_path():
    """
    `get_config` receives None as conf_path.
    The default folder in this case does not exists.
    We check in the raised error if the path concatenation is correct
    """
    try:
        conf_path = paths.get_config()
    except FileNotFoundError as e:
        assert str(e) == "Configuration file or directory './json_config/' not found"
    try:
        conf_path = paths.get_config(workspace="workspace")
    except FileNotFoundError as e:
        assert (
            str(e)
            == "Configuration file or directory 'workspace/json_config/' not found"
        )


"""
GET_DB_DIR
"""


def test_get_db_dir(ioc_dir):
    """
    `get_db_dir` receives a valid workspace.
    """
    db_dir = paths.get_db_dir(ioc_dir.path)
    assert db_dir == os.path.join(ioc_dir.path, "testApp/Db/")


def test_get_db_dir(empty_dir, ioc_dir_with_only_app):
    """
    `get_db_dir` receives an invalid workspaces.
    """
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


"""
GET_MAKEFILE
"""


def test_get_makefile(ioc_dir):
    """
    `get_makefile` receives a valid path.
    """
    makefile = paths.get_makefile(ioc_dir.getpath("testApp/Db"))
    assert makefile == os.path.join(ioc_dir.getpath("testApp/Db"), "Makefile")


def test_get_makefile_invalid():
    """
    `get_makefile` receives an invalid path.
    """
    try:
        makefile = paths.get_makefile("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1