import os
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from typer.testing import CliRunner
from gitease.cli import save, share, load, message, cli
from gitease.git_helper import GitHelper
from tests.utils import file_exists
import subprocess

TEST_REPO = "https://github.com/xdssio/gitease-testing-repo.git"


@pytest.fixture()
def mock_project():
    project = TemporaryDirectory()
    subprocess.run(f"git clone {TEST_REPO} {project.name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    Path(f"{project.name}/test_file.txt").write_text("This is a test file")
    Path(f"{project.name}/cloud_cli.txt").write_text("This is a test file")
    mock_project = project.name
    yield mock_project


def test_save(mock_project):
    os.chdir(mock_project)
    print(mock_project)
    print(os.getcwd())
    mock_runner = CliRunner()
    result = mock_runner.invoke(cli,
                                ["save", "--add", "test_file.txt", "--message", "Initial commit", "--quiet", "--yes"])
    assert result.exit_code == 0
    assert "Committed with message: Initial commit" in result.stdout


def test_share(mock_project):
    os.chdir(mock_project)
    mock_runner = CliRunner()
    result = mock_runner.invoke(cli, ["share", "--add", "cloud_cli.txt", "--message", "added cloud_cli.txt", "--quiet",
                                      "--yes"])
    assert result.exit_code == 0
    assert "Pushed changes to the cloud" in result.stdout
    assert file_exists(mock_project, "cloud_cli.txt")
    helper = GitHelper(mock_project)
    helper.reset(hard=True, commit='HEAD~1')
    helper.push(force=True)
    assert not file_exists(mock_project, "cloud_cli.txt")


def test_load(mock_project):
    os.chdir(mock_project)
    mock_runner = CliRunner()
    result = mock_runner.invoke(cli, ["load"])
    assert result.exit_code == 0
    assert "Already up to date." in result.stdout


def test_message(mock_project):
    os.chdir(mock_project)
    mock_runner = CliRunner()
    helper = GitHelper(mock_project)
    helper.stage(helper.get_changes())
    result = mock_runner.invoke(cli, ["message", '--quiet'])
    assert result.exit_code == 0
    assert result.stdout


def test_undo(mock_project):
    os.chdir(mock_project)
    mock_runner = CliRunner()
    helper = GitHelper(mock_project)
    helper.stage(helper.get_changes())
    result = mock_runner.invoke(cli, ["undo"], input="n")
    assert result.exit_code == 0
    assert "Ok, Bye!" in result.stdout
