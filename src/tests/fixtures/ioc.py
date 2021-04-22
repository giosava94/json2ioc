import pytest, os
from testfixtures import TempDirectory


@pytest.fixture
def subs_template_txt():
    return """# My example template

file db/example.template { pattern 
    { PREFIX,     SCAN }
    { "$(example_property)", "1 second"}
    { "$(example_property)", "3 second"}
}
"""


@pytest.fixture
def subs_template_txt_replaced():
    return """# My example template

file db/example.template { pattern 
    { PREFIX,     SCAN }
    { "example_value", "1 second"}
    { "example_value", "3 second"}
}
"""


@pytest.fixture()
def ioc_dir_with_only_app():
    with TempDirectory() as dir:
        dir.makedir("testApp")
        yield dir


@pytest.fixture()
def ioc_dir_with_only_iocboot():
    with TempDirectory() as dir:
        dir.makedir("iocBoot")
        yield dir


"""
IOC ioc type
"""


@pytest.fixture()
def ioc_dir_std():
    with TempDirectory() as dir:
        os.chdir(dir.path)
        os.system("makeBaseApp.pl -t ioc test")
        os.system("makeBaseApp.pl -i -p test -t ioc test")
        yield dir


@pytest.fixture()
def ioc_dir_std_with_subs_template(ioc_dir_std, subs_template_txt):
    ioc_dir_std.write("testApp/Db/template.substitutions", subs_template_txt, "utf-8")
    return ioc_dir_std


@pytest.fixture()
def ioc_dir_std_with_conf_dir(ioc_dir_std):
    ioc_dir_std.makedir("json_config")
    return ioc_dir_std


@pytest.fixture()
def makefile_std(ioc_dir_std):
    return ioc_dir_std.read("testApp/Db/Makefile", "utf-8")


@pytest.fixture()
def makefile_std_lines(makefile_std):
    return [i + "\n" for i in makefile_std.splitlines()]


@pytest.fixture()
def subs_template_lines(subs_template_txt):
    return [i + "\n" for i in subs_template_txt.splitlines()]


@pytest.fixture()
def st_cmd_std(ioc_dir_std):
    txt = ioc_dir_std.read("iocBoot/ioctest/st.cmd", "utf-8")
    return txt


@pytest.fixture()
def st_cmd_std_lines(st_cmd_std):
    return [i + "\n" for i in st_cmd_std.splitlines()]


"""
IOC example type
"""


@pytest.fixture()
def ioc_dir_example():
    with TempDirectory() as dir:
        os.chdir(dir.path)
        os.system("makeBaseApp.pl -t example test")
        os.system("makeBaseApp.pl -i -p test -t example test")
        yield dir


@pytest.fixture()
def ioc_dir_ex_with_subs_template(ioc_dir_example, subs_template_txt):
    ioc_dir_example.write(
        "testApp/Db/template.substitutions", subs_template_txt, "utf-8"
    )
    return ioc_dir_example
