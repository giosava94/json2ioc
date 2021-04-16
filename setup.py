from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="json2ioc",
    version="1.0",
    author="Savarese Giovanni",
    author_email="savarese.giovanni94@gmail.com",
    description="Create EPICS IOCs from json configurations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giosava94/json2ioc",
    project_urls={
        "Bug Tracker": "https://github.com/giosava94/json2ioc/issues",
        "Contributions": "https://github.com/giosava94/json2ioc/pulls",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={"console_scripts": ["json2ioc = json2ioc.__main__:main"]},
)
