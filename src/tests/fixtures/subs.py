import pytest

txt = """
$(example_property)
$(not_existing_macro)
{ string }
generic_string
"""

final_txt = """
example_value
$(not_existing_macro)
{ string }
generic_string
"""

makefile = """
DB += "prova.db"
"""

subs_lines = ["example.substitutions"]


@pytest.fixture()
def subs_template():
    return txt


@pytest.fixture()
def conf_obj():
    return {"example_name": {"example_property": "example_value"}}


@pytest.fixture()
def lines():
    return txt.splitlines()


@pytest.fixture()
def final_lines():
    return final_txt.splitlines()


@pytest.fixture()
def output_text():
    return final_txt


@pytest.fixture()
def makefile_lines():
    return makefile.splitlines()


@pytest.fixture()
def subs_list():
    return subs_lines