import pytest, json, os
from testfixtures import TempDirectory
import json2ioc.paths as paths


@pytest.fixture()
def ioc_dir():
    with TempDirectory() as dir:
        dir.makedir("testApp/Db")
        dir.makedir("iocBoot/ioctest")
        yield dir


@pytest.fixture()
def json_empty_conf_dir():
    with TempDirectory() as dir:
        dir.makedir("json_config")
        yield dir


@pytest.fixture()
def json_conf_dir():
    with TempDirectory() as dir:
        conf_data = {"example_name": {"example_property": "example_value"}}
        s = json.dumps(conf_data)
        p1 = "json_config/example.json"
        p2 = "json_config/example.txt"
        dir.write(p1, s, "utf-8")
        dir.write(p2, s, "utf-8")
        yield dir


@pytest.fixture()
def json_conf_json_file():
    with TempDirectory() as dir:
        conf_data = {"example_name": {"example_property": "example_value"}}
        s = json.dumps(conf_data)
        p = dir.write("example.json", s, "utf-8")
        yield p


@pytest.fixture()
def json_conf_not_json_file():
    with TempDirectory() as dir:
        conf_data = {"example_name": {"example_property": "example_value"}}
        s = json.dumps(conf_data)
        p = dir.write("example.txt", s, "utf-8")
        yield p


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
    except ValueError:
        assert 1


def test_get_conf_files_not_exist_file():
    """
    `gwt_conf_files` receives the name of a not existing file
    """
    try:
        files = paths.get_conf_files("not_existing.json")
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
        assert str(e) == "Configuration file or directory 'workspace/json_config/' not found"
