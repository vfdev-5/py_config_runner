from codecs import open as codecs_open
from setuptools import setup, find_packages
from config_runner import __version__

# Get the long description from the relevant file
with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="config_runner",
    version=__version__,
    description=u"Command line executable to run a script with python configuration file",
    long_description=long_description,
    author="vfdev-5",
    author_email="vfdev-5@gmail.com",
    packages=find_packages(exclude=['tests', 'examples', 'docs']),
    install_requires=[
        'click',
        'pathlib2;python_version<"3"'
    ],
    test_suite="tests",
    extras_require={'tests': ['pytest', 'pytest-cov']},
    entry_points="""
        [console_scripts]
            config_runner=config_runner.__main__:command
        """
)
