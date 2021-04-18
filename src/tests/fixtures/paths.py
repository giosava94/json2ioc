import pytest, json
from testfixtures import TempDirectory


@pytest.fixture()
def empty_dir():
    with TempDirectory() as dir:
        yield dir


@pytest.fixture()
def ioc_dir():
    with TempDirectory() as dir:
        dir.makedir("testApp/Db")
        dir.makedir("iocBoot/ioctest")
        yield dir


@pytest.fixture()
def ioc_dir_with_only_app():
    with TempDirectory() as dir:
        dir.makedir("testApp")
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
