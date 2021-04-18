import json2ioc.start_command as st_cmd
from fixtures.st_cmd import st_cmd_lines, st_cmd_indices


def test_get_st_cmd_relevant_indices(st_cmd_lines):
    """
    Test `get_st_cmd_relevant_indices`
    """

    # Receives a valid set of lines
    d = st_cmd.get_st_cmd_relevant_indices(st_cmd_lines)
    assert d["db_load_template_comment_line"] == 13
    assert d["env_paths_comment_line"] == 5

    # Receives empty list
    d = st_cmd.get_st_cmd_relevant_indices([])
    assert d["db_load_template_comment_line"] == 0
    assert d["env_paths_comment_line"] == 0

    # Invalid lines argument
    try:
        d = st_cmd.get_st_cmd_relevant_indices(None)
        assert 0
    except TypeError:
        assert 1


def test_generate_start_command(st_cmd_lines, st_cmd_indices):
    """
    Test `generate_start_command`
    """

    lines = st_cmd.generate_start_command(
        st_cmd_lines, st_cmd_indices, "example.substitutions"
    )
    assert len(lines) == len(st_cmd_lines) + 1

    # Receives a param that is invalid
    try:
        lines = st_cmd.generate_start_command(
            None, st_cmd_indices, "example.substitutions"
        )
        assert 0
    except TypeError:
        assert 1
    try:
        lines = st_cmd.generate_start_command(
            st_cmd_lines, None, "example.substitutions"
        )
        assert 0
    except TypeError:
        assert 1
    try:
        lines = st_cmd.generate_start_command(st_cmd_lines, st_cmd_indices, None)
        assert 0
    except TypeError:
        assert 1
