import re


def replace_text(inp_text, config, start=0, out_text=""):
    """
    Given an input text, and a configuration object,
    starting from the given index replace
    all the macros defined in the configuration.
    Append the result to the given output text string.
    Return the output text and the index of the last char,
    of the input text, taken into accout for the replacement.
    """

    inp_lines, end_idx = find_lines_to_replace(inp_text, start)
    restrict_text = inp_text[:end_idx]

    out_lines = []
    for item in config.values():
        out_lines += replace_macros(inp_lines, item)

    old_string = "".join(inp_lines)
    new_string = "".join(out_lines)
    out_text += restrict_text.replace(old_string, new_string, 1)

    return out_text, end_idx


def find_lines_to_replace(inp_text, start=0):
    """
    In the given input text, starting from the given start index,
    find all blocks of code, splitting them into lines,
    where the replace action must take place.
    Return the lines to replace and the last index
    of the text block to replace.
    """

    if type(inp_text) != str:
        raise TypeError(
            "'inp_text' must be str. Received type is '%s'" % type(inp_text)
        )
    if type(start) != int:
        msg = "'start' must be an int greater or equal than 0. "
        msg += "Received value is '%s'" % type(start)
        raise TypeError(msg)
    elif start < 0:
        msg = "'start' must be an int greater or equal than 0. "
        msg += "Received value is '%d'" % start
        raise TypeError(msg)

    inp_lines = []
    end = start
    counter = 0
    while end < len(inp_text) - 1:
        if inp_text[end] == "{":
            counter += 1
        elif inp_text[end] == "}":
            counter -= 1
            if counter == -1:
                break
        elif inp_text[end] == "\n":
            inp_lines.append(inp_text[start : end + 1])
            start = end + 1
        end += 1
    return inp_lines, end + 1


def replace_macros(inp_lines, item):
    """
    For each line find the macro and replace it with the correct value.
    Return the updated lines.
    """

    if type(inp_lines) != list:
        raise TypeError(
            "'inp_lines' expects a list. Found type is '%s'" % type(inp_lines)
        )
    if type(item) != dict:
        raise TypeError("'item' expects a dict. Found type is '%s'" % type(item))

    new_lines = inp_lines[:]
    for k, v in item.items():
        for i in range(len(inp_lines)):
            new_lines[i] = new_lines[i].replace("$(%s)" % k, v)
    return new_lines


def generate_substitutions(inp_text, conf):
    """
    From configuration object and input text,
    search the `{pattern {` string and then
    substitute macros and create substitutions file.
    """

    out_text = ""
    start_idx = 0
    target = re.compile(r"\{[\s]*pattern[\s]*\{[^\{]*", re.DOTALL)

    if target is None:
        raise Exception("Valid '{ pattern {' expression not found")

    while True:
        m = re.search(target, inp_text[start_idx:])
        if m is None:
            break
        out_text, end_idx = replace_text(inp_text[start_idx:], conf, m.end(), out_text)
        start_idx += end_idx

    return out_text


def add_subs_to_makefile(lines, subs_list):
    """
    Add to makefile lines new substitutions files
    Return the new lines to write.
    """

    new_lines = lines[:]
    i = 0
    for l, line in enumerate(new_lines):
        if "DB +=" in line:
            i = l
    for sub in subs_list:
        new_line = "DB += %s\n" % sub
        if new_line not in new_lines:
            new_lines.insert(i + 1, new_line)
            i += 1
    return new_lines
