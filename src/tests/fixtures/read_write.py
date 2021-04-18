import pytest, json
from testfixtures import TempDirectory


@pytest.fixture()
def json_file():
    with TempDirectory() as dir:
        conf_data = {"example_name": {"example_property": "example_value"}}
        s = json.dumps(conf_data)
        p = dir.write("example.json", s, "utf-8")
        yield {"path": p, "data": conf_data}


@pytest.fixture()
def invalid_json_file():
    with TempDirectory() as dir:
        conf_data = {"example_name": {"example_property": "example_value"}}
        s = json.dumps(conf_data)
        p = dir.write("example.json", s[5:-2], "utf-8")
        yield p


@pytest.fixture()
def text_file():
    with TempDirectory() as dir:
        lines = ["First line\n", "Second line\n"]
        text = "".join(lines)
        p = dir.write("text.txt", text, "utf-8")
        yield {"path": p, "lines": lines, "text": text}
