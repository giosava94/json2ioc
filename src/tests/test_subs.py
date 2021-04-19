from fixtures.subs import (
    subs_template,
    conf_obj,
    lines,
    final_lines,
    output_text,
    makefile_lines,
    subs_list,
)
import json2ioc.substitutions as subs


def test_replace_text(subs_template, conf_obj, output_text):
    """
    Test `replace_test`.
    """

    out_text, idx = subs.replace_text(subs_template, conf_obj)
    assert idx == len(subs_template)
    assert out_text == output_text


def test_find_lines_to_replace(subs_template):
    """
    Test `find_lines_to_replace`
    """

    lines, idx = subs.find_lines_to_replace(subs_template)
    assert len(lines) == 4
    assert idx == len(subs_template)


def test_replace_macros(lines, conf_obj, final_lines):
    """
    Test `replace_macros`
    """

    new_lines = subs.replace_macros(lines, conf_obj["example_name"])
    assert new_lines == final_lines


def test_generate_substitutions(subs_template, conf_obj, output_text):
    """
    Test `generate_substitutions`
    """

    out_text = subs.generate_substitutions(subs_template, conf_obj)
    assert out_text == output_text


def test_add_subs_to_makefile(makefile_lines, subs_list):
    """
    Test `add_subs_to_makefile`
    """

    new_lines = subs.add_subs_to_makefile(makefile_lines, subs_list)
    assert len(new_lines) == len(makefile_lines) + 1
