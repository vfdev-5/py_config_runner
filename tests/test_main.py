import pytest

from click.testing import CliRunner

from py_config_runner.__main__ import command, print_script_filepath


@pytest.fixture
def runner():
    return CliRunner()


def test_command(runner, script_filepath, config_filepath):  # noqa: F811
    cmd = [script_filepath.as_posix(), config_filepath.as_posix()]
    result = runner.invoke(command, cmd)
    assert result.exit_code == 0, repr(result) + "\n" + result.output
    assert "Run\n1\n2\n{}\n{}".format(config_filepath, script_filepath) in result.output


def test_print_script_filepath():
    print_script_filepath()


def test_command_on_example(runner, example_path, example_scripts_training, example_baseline_config):  # noqa: F811
    import sys

    sys.path.insert(0, example_path.as_posix())
    cmd = [example_scripts_training.as_posix(), example_baseline_config.as_posix()]
    result = runner.invoke(command, cmd)
    assert result.exit_code == 0, repr(result) + "\n" + result.output


def test_run_executable_as_script(example_path, example_scripts_training, example_baseline_config):  # noqa: F811
    import subprocess
    import os
    import sys

    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = "{}:{}".format(
        example_path.as_posix(), current_env["PYTHONPATH"] if "PYTHONPATH" in current_env else ""
    )

    from py_config_runner import __main__

    cmd = [
        sys.executable,
        __main__.__file__,
        example_scripts_training.as_posix(),
        example_baseline_config.as_posix(),
    ]
    process = subprocess.Popen(cmd, env=current_env)
    process.wait()
    assert process.returncode == 0, subprocess.CalledProcessError(returncode=process.returncode, cmd=cmd)
