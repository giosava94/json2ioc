from fixtures.ioc import (
    ioc_dir_std,
    subs_template_lines,
    subs_template_txt,
    subs_template_txt_replaced,
    st_cmd_std,
    st_cmd_std_lines,
    makefile_std,
    makefile_std_lines,
)
from fixtures.conf import conf_data
import json2ioc.substitutions as subs


def test_find_lines_to_replace_valid_template(subs_template_txt, st_cmd_std):
    """
    Find lines to replace.
    It does not check the file type or its content.
    It just makes some assumptions about
    the start char and the end char of the block.
    """
    lines, idx = subs.find_lines_to_replace(subs_template_txt)
    assert len(lines) > 0
    assert idx > 0

    lines, idx = subs.find_lines_to_replace(st_cmd_std)
    assert len(lines) > 0
    assert idx > 0

    lines, idx = subs.find_lines_to_replace("string")
    assert len(lines) == 0
    assert idx > 0

    lines, idx = subs.find_lines_to_replace("")
    assert len(lines) == 0
    assert idx > 0


def test_find_lines_to_replace_invalid_inp_text():
    """
    Receives and invalid argument
    """
    arg = None
    try:
        lines, idx = subs.find_lines_to_replace(arg)
        assert 0
    except TypeError as e:
        assert str(e) == "'inp_text' must be str. Received type is '%s'" % type(arg)

    arg = 1
    try:
        lines, idx = subs.find_lines_to_replace(arg)
        assert 0
    except TypeError as e:
        assert str(e) == "'inp_text' must be str. Received type is '%s'" % type(arg)

    arg = [1, 2, 3]
    try:
        lines, idx = subs.find_lines_to_replace(arg)
        assert 0
    except TypeError as e:
        assert str(e) == "'inp_text' must be str. Received type is '%s'" % type(arg)


def test_find_lines_to_replace_valid_start_idx():
    """
    Receives an invalid start argument
    """
    txt = "string"
    idx = len(txt) - 2
    lines, end = subs.find_lines_to_replace(txt, idx)
    assert len(lines) == 0
    assert end == len(txt)

    idx = len(txt) + 5
    lines, end = subs.find_lines_to_replace(txt, idx)
    assert len(lines) == 0
    assert end == idx + 1


def test_find_lines_to_replace_invalid_start_idx():
    """
    Receives an invalid start argument
    """
    txt = "string"
    idx = None
    try:
        lines, idx = subs.find_lines_to_replace(txt, idx)
        assert 0
    except TypeError as e:
        msg = "'start' must be an int greater or equal than 0. "
        msg += "Received value is '%s'" % type(idx)
        assert str(e) == msg

    idx = "string"
    try:
        lines, idx = subs.find_lines_to_replace(txt, idx)
        assert 0
    except TypeError as e:
        msg = "'start' must be an int greater or equal than 0. "
        msg += "Received value is '%s'" % type(idx)
        assert str(e) == msg

    idx = [1, 2, 3]
    try:
        lines, idx = subs.find_lines_to_replace(txt, idx)
        assert 0
    except TypeError as e:
        msg = "'start' must be an int greater or equal than 0. "
        msg += "Received value is '%s'" % type(idx)
        assert str(e) == msg

    idx = -1
    try:
        lines, idx = subs.find_lines_to_replace(txt, idx)
        assert 0
    except TypeError as e:
        msg = "'start' must be an int greater or equal than 0. "
        msg += "Received value is '%d'" % idx
        assert str(e) == msg


def test_replace_macros_valid_args(
    conf_data, subs_template_lines, subs_template_txt_replaced, st_cmd_std_lines
):
    """
    Receives valid arguments
    """

    new_lines = subs.replace_macros(subs_template_lines, conf_data["example_name"])
    final_txt = "".join(new_lines)
    assert final_txt == subs_template_txt_replaced

    new_lines = subs.replace_macros(st_cmd_std_lines, conf_data["example_name"])
    assert "".join(new_lines) == "".join(st_cmd_std_lines)

    new_lines = subs.replace_macros([], conf_data["example_name"])
    assert new_lines == []


def test_replace_macros_invalid_inp_lines(conf_data):
    """
    Receives invalid inp_lines arg
    """

    inp_lines = None
    try:
        new_lines = subs.replace_macros(inp_lines, conf_data["example_name"])
        assert 0
    except TypeError as e:
        assert str(e) == "'inp_lines' expects a list. Found type is '%s'" % type(
            inp_lines
        )

    inp_lines = None
    try:
        new_lines = subs.replace_macros(inp_lines, None)
        assert 0
    except TypeError as e:
        assert str(e) == "'inp_lines' expects a list. Found type is '%s'" % type(
            inp_lines
        )

    inp_lines = "string"
    try:
        new_lines = subs.replace_macros(inp_lines, conf_data["example_name"])
        assert 0
    except TypeError as e:
        assert str(e) == "'inp_lines' expects a list. Found type is '%s'" % type(
            inp_lines
        )

    inp_lines = 1
    try:
        new_lines = subs.replace_macros(inp_lines, conf_data["example_name"])
        assert 0
    except TypeError as e:
        assert str(e) == "'inp_lines' expects a list. Found type is '%s'" % type(
            inp_lines
        )


def test_replace_macros_invalid_configuration(subs_template_lines, conf_data):
    """
    Receives valid arguments
    """

    conf = None
    try:
        new_lines = subs.replace_macros(subs_template_lines, conf)
        assert 0
    except TypeError as e:
        assert str(e) == "'item' expects a dict. Found type is '%s'" % type(conf)

    conf = []
    try:
        new_lines = subs.replace_macros(subs_template_lines, conf)
        assert 0
    except TypeError as e:
        assert str(e) == "'item' expects a dict. Found type is '%s'" % type(conf)

    conf = 1
    try:
        new_lines = subs.replace_macros(subs_template_lines, conf)
        assert 0
    except TypeError as e:
        assert str(e) == "'item' expects a dict. Found type is '%s'" % type(conf)

    conf = "string"
    try:
        new_lines = subs.replace_macros(subs_template_lines, conf)
        assert 0
    except TypeError as e:
        assert str(e) == "'item' expects a dict. Found type is '%s'" % type(conf)

    try:
        new_lines = subs.replace_macros(subs_template_lines, conf_data)
        assert 0
    except TypeError as e:
        assert str(e) == "replace() argument 2 must be str, not dict"


def test_add_subs_to_makefile_valid_args(makefile_std_lines):
    """
    Receives valid_values
    """

    subs_list = []
    new_lines = subs.add_subs_to_makefile(makefile_std_lines, subs_list)
    assert len(new_lines) == len(makefile_std_lines) + len(subs_list)

    subs_list = ["example.substitutions"]
    new_lines = subs.add_subs_to_makefile(makefile_std_lines, subs_list)
    assert len(new_lines) == len(makefile_std_lines) + len(subs_list)

    subs_list = ["example1.substitutions", "example2.substitutions"]
    new_lines = subs.add_subs_to_makefile(makefile_std_lines, subs_list)
    assert len(new_lines) == len(makefile_std_lines) + len(subs_list)


# TODO: Add test functions for invalid values passed to add_subs_to_makefile

# TODO: Add test functions for replace_text
# def test_replace_text(subs_template_txt, conf_data, subs_template_txt_replaced):
#    """
#    Receives valid arguments
#    """
#    out_text, idx = subs.replace_text(subs_template_txt, conf_data)
#    assert idx == len(subs_template_txt)
#    assert out_text == subs_template_txt_replaced

# TODO: Add test functions for generate_substitutions after replace_text has been tested.
# def test_generate_substitutions_valid_args(
#    subs_template_txt, conf_data, subs_template_txt_replaced
# ):
#    """
#    Receives valid params
#    """
#    out_text = subs.generate_substitutions(subs_template_txt, conf_data)
#    print(out_text)
#    print(subs_template_txt_replaced)
#    assert out_text == subs_template_txt_replaced
