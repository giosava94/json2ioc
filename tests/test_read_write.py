import pytest, os, json
from testfixtures import TempDirectory
from json2ioc.read_write import (
    load_data_from_json,
    load_lines_from_file,
    load_text_from_file,
    write_lines_to_file,
    write_text_to_file,
)


@pytest.fixture()
def ioc_dir():
    with TempDirectory() as dir:
        dir.makedir("testApp/Db")
        dir.makedir("iocBoot/ioctest")
        yield dir


@pytest.fixture()
def ioc_single_conf_file(ioc_dir):
    conf_data = {"example_name": {"example_property": "example_value"}}
    s = json.dumps(conf_data)
    p = ioc_dir.write("example.json", s, "utf-8")
    yield {"path": p, "data": conf_data}


def test_load_data_from_json(ioc_single_conf_file):
    d = load_data_from_json(ioc_single_conf_file["path"])
    assert d == ioc_single_conf_file["data"]