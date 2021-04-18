import pytest

st_cmd_text = """#!../../bin/linux-x86_64/example

#- You may have to change example to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/example.dbd"
example_registerRecordDeviceDriver pdbbase

## Load record instances
#dbLoadRecords("db/xxx.db","user=sava")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=sava"
"""


@pytest.fixture()
def st_cmd_lines():
    lines = st_cmd_text.splitlines()
    return lines


@pytest.fixture()
def st_cmd_indices():
    return {
        "db_load_template_comment_line": 5,
        "env_paths_comment_line": 13,
    }