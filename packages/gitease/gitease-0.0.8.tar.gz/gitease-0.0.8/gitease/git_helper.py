import contextlib
import re
import subprocess
from typing import List
from pathlib import Path
from gitease.llm_helper import LanguageModel
import git
import os
import openai.error


class GitHelper:
    """
    A helper class for interacting with Git repositories.
    """

    def __init__(self, path: str = '.', verbose: bool = True):
        """
        Initializes a GitHelper instance.
        :param path: The path to the Git repository.
        :param verbose: Whether to print verbose output.
               """
        self.repo = git.Repo(path)
        self.verbose = verbose
        if not Path(path).joinpath('.git').exists():
            raise ValueError(f"Path {path} is not a git repo")
        if not Path(path).joinpath('.gitignore').exists():
            raise ValueError(f"Path {path} does not have a .gitignore file")

    def get_status(self):
        """
        Returns the Git status of the repository.
         :return: The Git status.
        """
        return self.repo.git.status(porcelain=True)

    def get_diff(self, staged: bool = False):
        """
        Returns the Git diff of the repository.
         :param staged: Whether to return the staged diff.
         :return: The Git diff.
        """
        if staged:
            return self.repo.git.diff('--staged')
        return self.repo.git.diff()

    def push(self, force: bool = False):
        """
        Pushes the repository to the remote.
         :return: The Git push output.
        """
        if force:
            return self.repo.git.push('--force')
        return self.repo.git.push()

    def pull(self):
        """
        Pulls the repository from the remote.
         :return: The Git pull output.
        """
        return self.repo.git.pull()

    def get_staged(self):
        """
        Returns the staged files.
         :return: The staged files.
        """
        staged = self.repo.git.diff('--staged', '--name-only').split('\n')
        if staged == ['']:
            staged = []
        return staged

    def stage(self, files: List[str] = None):
        """
        Stages the files.
         :param files: The files to stage.
        """
        if not files:
            return False
        self.repo.index.add(files)
        return True

    def unstage(self, files: List[str] = None):
        """
        Unstages the files.
         :param files: The files to unstage.
        """
        if not files:
            return False
        self.repo.git.restore(files, "--staged")
        return True

    def commit(self, message: str):
        self.repo.index.commit(message)
        return True

    def get_changes(self):
        """
        Returns a list of changed files in the repository.
        :return: The list of changed files.
        """

        files = []
        status = self.get_status()
        for line in status.split('\n'):
            if line.startswith('??') or line.strip().startswith('M'):
                files.append(line[3:])

        return files

    def summarize_diff(self, staged: bool = False):
        """
        Summarizes the Git diff of the repository.
         :param staged: Whether to summarize the staged diff.
        :return: The summarized diff.
        """
        if os.getenv("OPENAI_API_KEY") is None:
            raise RuntimeError(
                f"OPENAI_API_KEY not set - please set it in your environment variables or provide a commit message manually.")
        with contextlib.suppress(openai.error.InvalidRequestError):
            diff = self.get_diff(staged=staged)
            if diff:
                diff = LanguageModel(verbose=self.verbose).summarize(diff)
            return diff

        return "Diff too long to summarize."

    def reflog(self):
        return self.repo.git.reflog('show')


    def reset(self, hard: bool = False, commit:str=None ):
        args =[]
        if hard:
            args.append('--hard')
        if commit:
            args.append(commit)
        return self.repo.git.reset(*args)

    def remove(self, files: List[str] = None, commit:str=None):
        """
        Removes the files.
         :param files: The files to remove.
         :param commit: The commit message.
        """
        if not files:
            return False
        commit = commit or f"Removed files - {files}"
        self.repo.index.remove(files)
        self.repo.index.commit(commit)
        return True

