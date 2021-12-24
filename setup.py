import io
import os
import re

from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = read("README.md")

version = find_version("py_config_runner", "__init__.py")

requirements = [
    "click",
    "pydantic",
]


setup(
    name="py_config_runner",
    version=version,
    description="Python configuration file and command line executable to run a script with",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="vfdev-5",
    author_email="vfdev.5@gmail.com",
    url="https://github.com/vfdev-5/py_config_runner",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    install_requires=requirements,
    test_suite="tests",
    extras_require={"tests": ["pytest", "pytest-cov"]},
    entry_points="""
        [console_scripts]
            py_config_runner=py_config_runner.__main__:command
            py_config_runner_script=py_config_runner.__main__:print_script_filepath
        """,
)
