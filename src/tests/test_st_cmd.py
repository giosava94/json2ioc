import json2ioc.start_command as st_cmd
from fixtures.ioc import (
    ioc_dir_std,
    makefile_std,
    makefile_std_lines,
    st_cmd_std,
    st_cmd_std_lines,
)


def test_get_st_cmd_valid_lines(st_cmd_std_lines):
    """
    Receives a valid set of lines
    """
    d = st_cmd.get_st_cmd_relevant_indices(st_cmd_std_lines)
    assert d["db_load_template_comment_line"] > 0
    assert d["env_paths_comment_line"] > 0


def test_get_st_cmd_empty_lines():
    """
    Receives empty list
    """
    d = st_cmd.get_st_cmd_relevant_indices([])
    assert d["db_load_template_comment_line"] == 0
    assert d["env_paths_comment_line"] == 0


def test_get_st_cmd_valid_lines_no_target_info(makefile_std_lines):
    """
    Receives a valid set of lines but without the target information
    """
    d = st_cmd.get_st_cmd_relevant_indices(makefile_std_lines)
    assert d["db_load_template_comment_line"] == 0
    assert d["env_paths_comment_line"] == 0


def test_get_st_cmd_invalid_argument():
    """
    Invalid lines argument
    """
    arg = None
    try:
        d = st_cmd.get_st_cmd_relevant_indices(arg)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(arg)

    arg = 1
    try:
        d = st_cmd.get_st_cmd_relevant_indices(arg)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(arg)

    arg = "string"
    try:
        d = st_cmd.get_st_cmd_relevant_indices(arg)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(arg)


def test_generate_start_command_valid_arguments(st_cmd_std_lines):
    st_cmd_indices = {
        "db_load_template_comment_line": 5,
        "env_paths_comment_line": 13,
    }
    lines = st_cmd.generate_start_command(
        st_cmd_std_lines, st_cmd_indices, "example.substitutions"
    )
    offset = 0
    skip = False
    for i in range(len(st_cmd_std_lines)):
        j = i + offset
        if i == st_cmd_indices["env_paths_comment_line"]:
            assert lines[j] == "< envPaths"
        elif i == st_cmd_indices["db_load_template_comment_line"]:
            skip = True
        elif skip:
            if lines[j].startswith("#"):
                offset += 1
            else:
                offset -= 1
                skip = False
        else:
            assert st_cmd_std_lines[i] == lines[j]


def test_generate_start_command_invalid_lines_arguments():
    """
    Receives a lines param that is invalid
    """
    st_cmd_indices = {
        "db_load_template_comment_line": 5,
        "env_paths_comment_line": 13,
    }

    lines = None
    indices = None
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(lines)

    lines = None
    indices = st_cmd_indices
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(lines)

    lines = None
    indices = None
    subs = "example.substitutions"
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(lines)

    lines = 1
    indices = None
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(lines)

    lines = "string"
    indices = None
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'lines' expects a list. Found type is '%s'" % type(lines)


def test_generate_start_command_invalid_indices_arguments(st_cmd_std_lines):
    """
    Receives an indices param that is invalid
    """

    lines = st_cmd_std_lines
    indices = None
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'indices' expects a dict. Found type is '%s'" % type(indices)

    lines = st_cmd_std_lines
    indices = None
    subs = "example.substitutions"
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'indices' expects a dict. Found type is '%s'" % type(indices)

    lines = st_cmd_std_lines
    indices = 1
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'indices' expects a dict. Found type is '%s'" % type(indices)

    lines = st_cmd_std_lines
    indices = "string"
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'indices' expects a dict. Found type is '%s'" % type(indices)

    lines = st_cmd_std_lines
    indices = {"non-existing-word": 5}
    subs = "example.substitutions"

    out_lines = st_cmd.generate_start_command(lines, indices, subs)
    for i in range(len(lines)):
        assert lines[i] == out_lines[i]


def test_generate_start_command_invalid_subs_arguments(st_cmd_std_lines):
    """
    Receives a subs param that is invalid
    """
    st_cmd_indices = {
        "db_load_template_comment_line": 5,
        "env_paths_comment_line": 13,
    }

    lines = st_cmd_std_lines
    indices = st_cmd_indices
    subs = None
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'subs' expects a str. Found type is '%s'" % type(subs)

    lines = st_cmd_std_lines
    indices = st_cmd_indices
    subs = 1
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'subs' expects a str. Found type is '%s'" % type(subs)

    lines = st_cmd_std_lines
    indices = st_cmd_indices
    subs = ["string"]
    try:
        out_lines = st_cmd.generate_start_command(lines, indices, subs)
        assert 0
    except TypeError as e:
        assert str(e) == "'subs' expects a str. Found type is '%s'" % type(subs)
