import json, os
import json2ioc.read_write as rw
from fixtures.conf import (
    conf_data,
    conf_file,
    conf_file_not_valid,
    conf_file_not_json,
    empty_dir,
)
from fixtures.ioc import (
    ioc_dir_std,
    ioc_dir_std_with_subs_template,
    subs_template_lines,
    subs_template_txt,
)


def test_load_data_from_json_valid_path(conf_file, conf_file_not_json):
    """
    Receives a valid path to a json file.
    .json extension is not mandatory
    """
    d = rw.load_data_from_json(conf_file)
    key = d.get("example_name")
    assert not key is None
    assert key.get("example_property") == "example_value"

    d = rw.load_data_from_json(conf_file_not_json)
    key = d.get("example_name")
    assert not key is None
    assert key.get("example_property") == "example_value"


def test_load_data_from_json_invalid_path():
    """
    Receives an invalid path to a json file.
    """
    try:
        d = rw.load_data_from_json("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_load_data_from_json_incorrect_file(conf_file_not_valid):
    """
    Receives path to an invalid json file or a not json file
    """
    try:
        d = rw.load_data_from_json(conf_file_not_valid)
        assert 0
    except json.JSONDecodeError:
        assert 1


def test_load_lines_from_file_valid_path(
    ioc_dir_std_with_subs_template, subs_template_lines
):
    """
    Receives a valid path to a file.
    """
    path = ioc_dir_std_with_subs_template.getpath("testApp/Db/template.substitutions")
    d = rw.load_lines_from_file(path)
    for i in range(len(d)):
        assert d[i] == subs_template_lines[i]


def test_load_lines_from_file_invalid_path():
    """
    Receives an invalid path to a file.
    """
    try:
        d = rw.load_lines_from_file("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_load_text_from_file_valid_path(
    ioc_dir_std_with_subs_template, subs_template_txt
):
    """
    Receives a path to a file.
    """
    path = ioc_dir_std_with_subs_template.getpath("testApp/Db/template.substitutions")
    d = rw.load_text_from_file(path)
    assert d == subs_template_txt


def test_load_text_from_file_invalid_path():
    """
    Receives an invalid path to a file.
    """
    try:
        d = rw.load_text_from_file("invalid_path")
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_lines_to_file_success(empty_dir):
    """
    Receives a path to a file and a list.
    """
    path = empty_dir.path
    rw.write_lines_to_file(path + "valid.txt", [])
    assert 1
    rw.write_lines_to_file(path + "valid.txt", ["example line 1"])
    assert 1
    rw.write_lines_to_file(path + "valid.txt", ["example line 1", "example line 2"])
    assert 1


def test_write_lines_to_file_invalid_path():
    """
    Receives an invalid path to a file and a list.
    """
    lines = ["example line 1"]
    try:
        rw.write_lines_to_file("invalid_path/file.txt", lines)
        assert 0
    except FileNotFoundError:
        assert 1

    lines = "string"
    try:
        rw.write_lines_to_file("invalid_path/file.txt", lines)
        assert 0
    except TypeError as e:
        assert str(e) == "Received lines value '%s' is not a list" % lines


def test_write_lines_to_file_invalid_lines():
    """
    Receives invalid arguments to write as lines.
    """
    lines = None
    try:
        rw.write_lines_to_file("file.txt", lines)
        assert 0
    except TypeError as e:
        assert str(e) == "Received lines value '%s' is not a list" % lines

    lines = 1
    try:
        rw.write_lines_to_file("file.txt", lines)
        assert 0
    except TypeError as e:
        assert str(e) == "Received lines value '%s' is not a list" % lines

    lines = "string"
    try:
        rw.write_lines_to_file("file.txt", lines)
        assert 0
    except TypeError as e:
        assert str(e) == "Received lines value '%s' is not a list" % lines


def test_write_text_to_file_success(empty_dir):
    """
    Receives a path to a file and a text.
    """
    path = empty_dir.path
    rw.write_text_to_file(path + "valid.txt", "")
    assert 1
    rw.write_text_to_file(path + "valid.txt", "example text 1")
    assert 1


def test_write_text_to_file_invalid_path():
    """
    Receives an invalid path to a file and a text.
    """
    text = "example string"
    try:
        rw.write_text_to_file("invalid_path/file.txt", text)
        assert 0
    except FileNotFoundError:
        assert 1
        text = ["string"]

    try:
        rw.write_text_to_file("invalid_path/file.txt", text)
        assert 0
    except FileNotFoundError:
        assert 1


def test_write_text_to_file_invalid_text(empty_dir):
    """
    Receives invalid arguments to write as text.
    """
    path = empty_dir.path
    text = None
    try:
        rw.write_text_to_file(path + "file.txt", text)
        assert 0
    except TypeError:
        assert 1

    text = 1
    try:
        rw.write_text_to_file(path + "file.txt", text)
        assert 0
    except TypeError:
        assert 1

    text = ["string"]
    try:
        rw.write_text_to_file(path + "file.txt", text)
        assert 0
    except TypeError:
        assert 1
