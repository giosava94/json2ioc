from json2ioc.parser import parser


def test_parser():
    p = parser([])
    assert p.config is None
    assert not p.make
    assert p.st_cmd_out is None
    assert p.st_cmd_template is None
    assert p.subs_out is None
    assert p.subs_template is None
    assert p.workspace == "."

    p = parser(["--config", "path"])
    assert p.config == "path"
    p = parser(["-c", "path"])
    assert p.config == "path"
    try:
        p == parser(["-c", 1])
        assert 0
    except TypeError:
        assert 1

    p = parser(["--make"])
    assert p.make
    p = parser(["-m"])
    assert p.make
    try:
        p == parser(["-m", 1])
        assert 0
    except TypeError:
        assert 1
    try:
        p == parser(["-m", "1"])
        assert 0
    except SystemExit:
        assert 1

    p = parser(["--st-cmd-out", "path"])
    assert p.st_cmd_out == "path"
    p = parser(["-O", "path"])
    assert p.st_cmd_out == "path"
    try:
        p == parser(["-o", 1])
        assert 0
    except TypeError:
        assert 1

    p = parser(["--st-cmd-template", "path"])
    assert p.st_cmd_template == "path"
    p = parser(["-T", "path"])
    assert p.st_cmd_template == "path"
    try:
        p == parser(["-T", 1])
        assert 0
    except TypeError:
        assert 1

    p = parser(["--subs-out", "path"])
    assert p.subs_out == "path"
    p = parser(["-o", "path"])
    assert p.subs_out == "path"
    try:
        p == parser(["-o", 1])
        assert 0
    except TypeError:
        assert 1

    p = parser(["--subs-template", "path"])
    assert p.subs_template == "path"
    p = parser(["-t", "path"])
    assert p.subs_template == "path"
    try:
        p == parser(["-t", 1])
        assert 0
    except TypeError:
        assert 1

    p = parser(["--workspace", "path"])
    assert p.workspace == "path"
    p = parser(["-w", "path"])
    assert p.workspace == "path"
    try:
        p == parser(["-w", 1])
        assert 0
    except TypeError:
        assert 1

    try:
        p = parser(["--not-existing-param"])
        assert 0
    except SystemExit:
        assert 1
