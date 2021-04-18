import pytest, json
import json2ioc.read_write as rw
from fixtures.read_write import json_file, invalid_json_file, text_file


def test_load_data_from_json(json_file):
    """
    `load_data_from_json` receives a valid path to a json file.
    """
    d = rw.load_data_from_json(json_file["path"])
    assert d == json_file["data"]


def test_load_data_from_json_invalid_path():
    """
    `load_data_from_json` receives an invalid path to a json file.
    """
    try:
        d = rw.load_data_from_json("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_load_data_from_invlid_json(invalid_json_file):
    """
    `load_data_from_json` receives path to an invalid json file.
    """
    try:
        d = rw.load_data_from_json(invalid_json_file)
        assert 0
    except json.JSONDecodeError:
        assert 1


def test_load_lines_from_file(text_file):
    """
    `load_lines_from_file` receives a valid path to a file.
    """
    d = rw.load_lines_from_file(text_file["path"])
    for i in range(len(d)):
        assert d[i] == text_file["lines"][i]


def test_load_lines_from_file_invalid_path():
    """
    `load_lines_from_file` receives an invalid path to a file.
    """
    try:
        d = rw.load_lines_from_file("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_load_text_from_file(text_file):
    """
    `load_text_from_file` receives a path to a file.
    """
    d = rw.load_text_from_file(text_file["path"])
    assert d == text_file["text"]


def test_load_text_from_file_invalid_path():
    """
    `load_text_from_file` receives an invalid path to a file.
    """
    try:
        d = rw.load_text_from_file("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_lines_to_file(text_file):
    """
    `write_lines_to_file` receives a path to a file and a list.
    """
    rw.write_lines_to_file(text_file["path"], text_file["lines"])
    assert 1


def test_write_lines_to_invalid_file(text_file):
    """
    `write_lines_to_file` receives an invalid path to a file and a list.
    """
    try:
        rw.write_lines_to_file("invalid/file.txt", text_file["lines"])
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_lines_to_file_not_list_params(text_file):
    """
    `write_lines_to_file` receives a path to a file
    and try to write values that ar not lists.
    """
    rw.write_lines_to_file(text_file["path"], "string")
    assert 1
    try:
        rw.write_lines_to_file(text_file["path"], 2)
        assert 0
    except TypeError:
        assert 1


def test_write_invalid_lines_to_invalid_file():
    """
    `write_lines_to_file` receives an invalid path to a file
    and invalid argument as list.
    """
    try:
        rw.write_lines_to_file("invalid/file.txt", 2)
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_text_to_file(text_file):
    """
    `write_text_to_file` receives a path to a file and a text.
    """
    rw.write_text_to_file(text_file["path"], text_file["text"])
    assert 1


def test_write_text_to_invalid_file(text_file):
    """
    `write_text_to_file` receives an invalid path to a file and a text.
    """
    try:
        rw.write_text_to_file("invalid/file.txt", text_file["text"])
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_text_to_file_not_list_params(text_file):
    """
    `write_text_to_file` receives a path to a file
    and try to write values that ar not strings.
    """
    try:
        rw.write_text_to_file(text_file["path"], ["string"])
        assert 0
    except TypeError:
        assert 1
    try:
        rw.write_text_to_file(text_file["path"], 2)
        assert 0
    except TypeError:
        assert 1


def test_write_invalid_text_to_invalid_file():
    """
    `write_text_to_file` receives an invalid path to a file
    and invalid argument as text.
    """
    try:
        rw.write_text_to_file("invalid/file.txt", 2)
        assert 0
    except FileNotFoundError:
        assert 1
