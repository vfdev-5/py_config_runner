from codecs import open as codecs_open
from setuptools import setup, find_packages
from py_config_runner import __version__

# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="py_config_runner",
    version=__version__,
    description=u"Command line executable to run a script with Python configuration file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="vfdev-5",
    author_email="vfdev.5@gmail.com",
    url="https://github.com/vfdev-5/py_config_runner",
    packages=find_packages(exclude=['tests', 'examples', 'docs']),
    install_requires=[
        'click',
        'pathlib2;python_version<"3"'
    ],
    test_suite="tests",
    extras_require={'tests': ['pytest', 'pytest-cov']},
    entry_points="""
        [console_scripts]
            py_config_runner=py_config_runner.__main__:command
            py_config_runner_script=py_config_runner.__main__:print_script_filepath
        """
)
