import pytest

from click.testing import CliRunner

from py_config_runner.__main__ import command, print_script_filepath


@pytest.fixture
def runner():
    return CliRunner()


def test_command(runner, script_filepath, config_filepath):  # noqa: F811

    cmd = [script_filepath, config_filepath]
    result = runner.invoke(command, cmd)
    assert result.exit_code == 0, repr(result) + "\n" + result.output
    assert "Run\n1\n2\n{}\n{}".format(config_filepath, script_filepath) in result.output


def test_print_script_filepath():
    print_script_filepath()
