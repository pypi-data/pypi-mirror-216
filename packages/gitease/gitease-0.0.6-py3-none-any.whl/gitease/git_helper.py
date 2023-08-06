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
            staged = '--staged'
        return self.repo.git.diff(staged)

    def push(self):
        """
        Pushes the repository to the remote.
         :return: The Git push output.
        """

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
        return self.repo.git.diff('--staged', '--name-only').split('\n')

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

    def add_commit(self, files: List[str] = None, message: str = None):
        """
        Adds and commits changes to the repository.
         :param files: The list of files to add and commit. If None, all changes will be added and committed.
         :param message: The commit message.
        :return: True if changes were added and committed, False otherwise.
        """
        if not files:
            new_files, changed_files = self.get_changes()
            files = new_files + changed_files
        if not files:
            print("No changes found")
            return False

        if message is None:
            message = self.summarize_diff(staged=True)
            message = message + f"\n{self._join_files(files)}"
        if self.verbose:
            print(f"Adding files to git: {files}")
        self.repo.index.add(files)
        if self.verbose:
            print(message)
        self.repo.index.commit(message)
        return True

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
            return LanguageModel(verbose=self.verbose).summarize(self.get_diff(staged=staged))
        return "Diff too long to summarize."

    def reflog(self):
        return self.repo.git.reflog('show')

    def restore(self, files: List[str] = None):
        if not files:
            return False
        command = f"(cd {self.repo.working_tree_dir} && git restore --staged {' '.join(files)})"
        subprocess.run(command, shell=True)
        return True
