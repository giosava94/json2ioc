import json
import json2ioc.read_write as rw
from fixtures.read_write import json_text_dir, text_lines


def test_load_data_from_json(json_text_dir):
    """
    Test `load_data_from_json`.
    """

    # Receives a valid path to a json file.
    d = rw.load_data_from_json(json_text_dir.getpath("correct.json"))
    key = d.get("example_name")
    assert not key is None
    assert key.get("example_property") == "example_value"

    # Receives an invalid path to a json file.
    try:
        d = rw.load_data_from_json("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1

    # Receives path to an invalid json file.
    try:
        d = rw.load_data_from_json(json_text_dir.getpath("incorrect.json"))
        assert 0
    except json.JSONDecodeError:
        assert 1


def test_load_lines_from_file(json_text_dir):
    """
    Test `load_lines_from_file`.
    """

    # Receives a valid path to a file.
    d = rw.load_lines_from_file(json_text_dir.getpath("text.txt"))
    for i in range(len(d)):
        assert d[i] == text_lines[i]

    # Receives an invalid path to a file.
    try:
        d = rw.load_lines_from_file("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_load_text_from_file(json_text_dir):
    """
    Test `load_text_from_file`
    """

    # Receives a path to a file.
    d = rw.load_text_from_file(json_text_dir.getpath("text.txt"))
    assert d == "".join(text_lines)

    # Receives an invalid path to a file.
    try:
        d = rw.load_text_from_file("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_lines_to_file(json_text_dir):
    """
    Test `write_lines_to_file`.
    """

    # Receives a path to a file and a list.
    valid_path = json_text_dir.getpath("text.txt")
    invalid_path = "invalid_path/file.txt"
    rw.write_lines_to_file(valid_path, text_lines)
    assert 1

    # Receives an invalid path to a file and a list.
    try:
        rw.write_lines_to_file(invalid_path, text_lines)
        assert 0
    except FileNotFoundError:
        assert 1

    # Receives a path to a file and try to write values that ar not lists.
    rw.write_lines_to_file(valid_path, "string")
    assert 1
    try:
        rw.write_lines_to_file(valid_path, 2)
        assert 0
    except TypeError:
        assert 1

    # Receives an invalid path to a file and invalid argument as list.
    try:
        rw.write_lines_to_file(invalid_path, 2)
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_text_to_file(json_text_dir):
    """
    Test `write_text_to_file`.
    """

    # Receives a path to a file and a text
    valid_path = json_text_dir.getpath("text.txt")
    invalid_path = "invalid_path/file.txt"
    text = "".join(text_lines)
    rw.write_text_to_file(valid_path, text)
    assert 1

    # Receives an invalid path to a file and a text.
    try:
        rw.write_text_to_file(invalid_path, text)
        assert 0
    except FileNotFoundError:
        assert 1

    # Receives a path to a file and try to write values that ar not strings.
    try:
        rw.write_text_to_file(valid_path, ["string"])
        assert 0
    except TypeError:
        assert 1
    try:
        rw.write_text_to_file(valid_path, 2)
        assert 0
    except TypeError:
        assert 1

    # Receives an invalid path to a file and invalid argument as text.
    try:
        rw.write_text_to_file(invalid_path, 2)
        assert 0
    except FileNotFoundError:
        assert 1
