from tests.utils import file_exists


def test_file_exists(mock_helper):
    assert file_exists(mock_helper.repo.working_dir, "README.md")
    assert not file_exists(mock_helper.repo.working_dir, "README.m")
