import pytest, json, os
from testfixtures import TempDirectory


@pytest.fixture()
def conf_data():
    return {"example_name": {"example_property": "example_value"}}


@pytest.fixture()
def empty_dir():
    with TempDirectory() as dir:
        yield dir


@pytest.fixture()
def conf_dir_empty(empty_dir):
    empty_dir.makedir("json_config")
    return empty_dir


@pytest.fixture()
def conf_dir(conf_dir_empty, conf_data):
    s = json.dumps(conf_data)
    p1 = "json_config/example.json"
    p2 = "json_config/example.txt"
    conf_dir_empty.write(p1, s, "utf-8")
    conf_dir_empty.write(p2, s, "utf-8")
    return conf_dir_empty


@pytest.fixture()
def conf_file(conf_data):
    with TempDirectory() as dir:
        s = json.dumps(conf_data)
        p = dir.write("example.json", s, "utf-8")
        yield p


@pytest.fixture()
def conf_file_not_json(conf_data):
    with TempDirectory() as dir:
        s = json.dumps(conf_data)
        p = dir.write("example.txt", s, "utf-8")
        yield p


@pytest.fixture()
def conf_file_not_valid(conf_data):
    with TempDirectory() as dir:
        s = json.dumps(conf_data)
        p = dir.write("incorrect.json", s[5:-2], "utf-8")
        yield p
