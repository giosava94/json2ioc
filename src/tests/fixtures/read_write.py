import pytest, json
from testfixtures import TempDirectory

text_lines = ["First line\n", "Second line\n"]


@pytest.fixture()
def json_text_dir():
    with TempDirectory() as dir:
        conf_data = {"example_name": {"example_property": "example_value"}}
        s = json.dumps(conf_data)
        dir.write("correct.json", s, "utf-8")
        dir.write("incorrect.json", s[5:-2], "utf-8")
        text = "".join(text_lines)
        p = dir.write("text.txt", text, "utf-8")
        yield dir
