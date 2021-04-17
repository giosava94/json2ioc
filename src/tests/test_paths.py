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


def test_get_conf_files_dir_len0(json_empty_conf_dir):
    files = paths.get_conf_files(os.path.join(json_empty_conf_dir.path, "json_config"))
    assert len(files) == 0


def test_get_conf_files_dir_len1(json_conf_dir):
    files = paths.get_conf_files(os.path.join(json_conf_dir.path, "json_config"))
    assert len(files) == 1


def test_get_conf_files_json_file(json_conf_json_file):
    files = paths.get_conf_files(json_conf_json_file)
    assert len(files) == 1


def test_get_conf_files_not_json_file(json_conf_not_json_file):
    try:
        files = paths.get_conf_files(json_conf_not_json_file)
    except ValueError:
        assert 1
