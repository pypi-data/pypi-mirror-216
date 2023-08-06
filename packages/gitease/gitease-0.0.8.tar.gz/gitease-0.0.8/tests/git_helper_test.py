import pytest
from gitease.git_helper import GitHelper
from tests.utils import file_exists, TEST_REPO
from tempfile import TemporaryDirectory
import os
from pathlib import Path


@pytest.fixture
def mock_helper():
    project = TemporaryDirectory()
    os.system(f"git clone {TEST_REPO} {project.name}")
    mock_helper = GitHelper(path=project.name, verbose=False)
    yield GitHelper(path=project.name)


def test_get_status(mock_helper):
    assert mock_helper.get_status() == ''


def test_get_diff(mock_helper):
    assert mock_helper.get_diff() == ''
    Path(f"{mock_helper.repo.working_dir}/test_file.txt").touch()
    mock_helper.stage(["test_file.txt"])
    assert mock_helper.get_diff(True).startswith('diff --git a/test_file.txt b/test_file.txt')


def test_pull(mock_helper):
    assert mock_helper.pull() == 'Already up to date.'


def test_staging(mock_helper):
    assert mock_helper.get_changes() == []
    assert mock_helper.get_staged() == []

    Path(f"{mock_helper.repo.working_dir}/test_file.txt").touch()
    changes = mock_helper.get_changes()
    assert changes == ["test_file.txt"]
    assert mock_helper.get_staged() == []

    mock_helper.stage(changes)
    assert mock_helper.get_staged() == changes
    assert mock_helper.get_changes() == []

    mock_helper.unstage(changes)
    assert mock_helper.get_staged() == []
    assert mock_helper.get_changes() == ["test_file.txt"]


def test_summarize_diff(mock_helper):
    assert mock_helper.summarize_diff() == ''
    Path(f"{mock_helper.repo.working_dir}/test_file.txt").write_text("This is a test file")
    mock_helper.stage(["test_file.txt"])
    assert mock_helper.summarize_diff() == ''
    assert len(mock_helper.summarize_diff(staged=True)) > 0


def test_reflog(mock_helper):
    Path(f"{mock_helper.repo.working_dir}/test_file.txt").write_text("This is a test file")
    mock_helper.stage(["test_file.txt"])
    assert 'HEAD' in mock_helper.reflog()


def test_push(mock_helper):
    Path(f"{mock_helper.repo.working_dir}/test_cloud.txt").write_text("This is a test file")
    mock_helper.stage(["test_cloud.txt"])
    assert mock_helper.commit("Test commit")
    mock_helper.push()
    file_exists(mock_helper.repo.working_dir, "test_cloud.txt")
    assert mock_helper.get_status() == ''
    mock_helper.reset(hard=True, commit='HEAD~1')
    assert mock_helper.get_changes() == []
    mock_helper.push("--force")
    assert not file_exists(mock_helper.repo.working_dir, "test_cloud.txt")
