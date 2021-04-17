import pytest, json
from testfixtures import TempDirectory
import json2ioc.read_write as rw


@pytest.fixture()
def json_file():
    with TempDirectory() as dir:
        conf_data = {"example_name": {"example_property": "example_value"}}
        s = json.dumps(conf_data)
        p = dir.write("example.json", s, "utf-8")
        yield {"path": p, "data": conf_data}


@pytest.fixture()
def text_file():
    with TempDirectory() as dir:
        lines = ["First line\n", "Second line\n"]
        text = "".join(lines)
        p = dir.write("text.txt", text, "utf-8")
        yield {"path": p, "lines": lines, "text": text}


def test_load_data_from_json(json_file):
    d = rw.load_data_from_json(json_file["path"])
    assert d == json_file["data"]


def test_load_lines_from_file(text_file):
    d = rw.load_lines_from_file(text_file["path"])
    for i in range(len(d)):
        assert d[i] == text_file["lines"][i]


def test_load_text_from_file(text_file):
    d = rw.load_text_from_file(text_file["path"])
    assert d == text_file["text"]


def test_write_lines_to_file(text_file):
    rw.write_lines_to_file(text_file["path"], text_file["lines"])
    assert 1


def test_write_text_to_file(text_file):
    rw.write_text_to_file(text_file["path"], text_file["text"])
    assert 1
