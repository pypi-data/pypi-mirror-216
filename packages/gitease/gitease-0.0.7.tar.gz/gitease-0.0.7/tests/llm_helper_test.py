import pytest
from gitease.llm_helper import LanguageModel, RevertCommand


@pytest.fixture
def language_model():
    language_model = LanguageModel(verbose=False, temperature=0)
    return language_model


def test_summarize(language_model):
    text = "This is a sample text to be summarized."
    summary = language_model.summarize(text)
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_get_git_undo(language_model):
    reflog = "HEAD@{1}: commit: Initial commit"
    revert_command = language_model.get_git_undo(reflog)
    assert isinstance(revert_command, RevertCommand)
    assert revert_command.action == "Initial commit"
    assert revert_command.revert_command in ("git revert HEAD@{1}", 'git reset --hard HEAD@{1}')
