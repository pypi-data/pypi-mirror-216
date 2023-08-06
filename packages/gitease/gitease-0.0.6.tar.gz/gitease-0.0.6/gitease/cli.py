import typer
import os

from typing import List, Union
from rich.style import Style
from rich.console import Console
from rich.prompt import Prompt
from typing_extensions import Annotated
from gitease.git_helper import GitHelper
from gitease.llm_helper import LanguageModel

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
cli = typer.Typer(add_completion=False)
console = Console()
console.print("Welcome to GitEase", style=Style(color="green", blink=True, bold=True))

add_annotation = Annotated[List[str], typer.Option("--add", "-a", help="Files to add. All of not provided")]
message_annotation = Annotated[str, typer.Option("--message", "-m",
                                                 help=f"commit message - If not provided, Generate by AI (given OPENAI_API_KEY is set)")]
quiet_annotation = Annotated[
    bool, typer.Option("--quiet", "-q", help="If True - Quiet the the LLM thoughts and other messages")]
y_annotation = Annotated[bool, typer.Option("--yes", "-y", help="If True - Skips confirmation message")]


def _join_files(files):
    return '\n'.join(files)


def is_valid(values: Union[List[str], str, None]):
    return values is not None and values != "" and len(values) > 0 and values[0] != ""


def get_user_message(diff):
    if not diff:
        return None
    console.print("\nHere is the diff:\n", style=Style(color="red", blink=True, bold=True))
    diffs = diff.split("diff --git")
    for change in diffs:
        console.print("diff --git" + change, style=Style())
    console.print("Provide a commit message", style=Style(color="yellow"))
    console.print("Press CTRL+C to cancel", style=Style(color="red"))
    return Prompt.ask("Message")


def confirm_message(message):
    console.print(f"\nYour commit message is:\n{message}\n")
    console.print("To confirm, press Enter.", style=Style(color="green"))
    console.print("Otherwise, write your own message:", style=Style(color="yellow"))
    console.print("Press CTRL+C to cancel", style=Style(color="red"))
    return Prompt.ask("Response")


def get_message(helper: GitHelper, quiet: bool, y: bool):
    message = None
    diff = helper.get_diff(staged=True)
    if diff:
        try:
            if OPENAI_API_KEY:
                message = LanguageModel(verbose=not quiet).summarize(diff).lstrip()
                # message = message + f"\n{_join_files(add)}"
                if not y:
                    response = confirm_message(message)
                    if response and len(response) > 0:  # new user commit message
                        message = response
            else:
                message = get_user_message(diff)
        except KeyboardInterrupt:
            console.print("Cancelled", style=Style(color="red", blink=True, bold=True))
            message = None
    return message


def get_stage(helper: GitHelper, stage_at_end: List[str] = None):
    staged_at_start = None
    if is_valid(stage_at_end):  # ignore files that are not requested to be added
        staged_at_start = helper.get_staged()
        helper.unstage(staged_at_start)
    else:
        stage_at_end = helper.get_changes()

    if is_valid(stage_at_end):  # might not have changes
        helper.stage(stage_at_end)
    return staged_at_start, stage_at_end


@cli.command()
def save(add: add_annotation = None,
         message: message_annotation = None,
         quiet: quiet_annotation = False,
         y: y_annotation = False):
    """
    Add and commit files to git.
    """
    helper = GitHelper(verbose=not quiet)
    staged_at_start, staged_at_end = get_stage(helper, add)
    if not is_valid(staged_at_end):
        console.print("No changes files to add", style=Style(color="red", blink=True, bold=True))

    if not is_valid(message):
        message = get_message(helper, quiet, y)

    if is_valid(message):
        helper.commit(message)
        console.print(f"Committed with message: {message}")
    if is_valid(staged_at_start):  # cleanup
        helper.unstage(add)
        helper.stage(staged_at_start)


@cli.command()
def share(add: add_annotation = None,
          message: message_annotation = None,
          quiet: quiet_annotation = False,
          y: y_annotation = False):
    """Share to remote: add, commit and push to git"""
    save(add=add, message=message, quiet=quiet, y=y)
    GitHelper(verbose=not quiet).push()
    console.print("Pushed changes to the cloud", style=Style(color="green", blink=True, bold=True))



@cli.command()
def load():
    """Pull recent updates from git"""
    GitHelper().pull()


@cli.command()
def message(quiet: quiet_annotation = False,
            copy: Annotated[bool, typer.Option("--copy", "-c", help="Copy to clipboard")] = False):
    """Generate commit message from diff using AI"""
    if not OPENAI_API_KEY:
        console.print(f"OPENAI_API_KEY not set", style=Style(color="red", blink=True, bold=True))
        return False
    diff = GitHelper(verbose=not quiet).get_diff(staged=True)
    message = LanguageModel(verbose=not quiet).summarize(diff).lstrip()
    console.print("Commit message:\n", style=Style(color="red", blink=True, bold=True))
    console.print(message)
    if copy:
        try:
            import clipboard
            console.print("Copied to clipboard", style=Style(color="green"))
            clipboard.copy(message)
        except ImportError:
            console.print("Install clipboard to copy to clipboard: 'pip install clipboard'",
                          style=Style(color="red", blink=True, bold=True))


@cli.command()
def undo():
    """Undo last git action"""
    llm = LanguageModel()
    reflog = "\n".join(GitHelper().reflog().split("\n")[0])
    last_action = llm.get_git_undo(reflog)
    console.print(f"Last git action is: [purple]{last_action.action}[/purple]", style=Style(color="yellow"))
    console.print(f"A revert command is: [red]{last_action.revert_command}[/red]", style=Style(color="yellow"))
    response = Prompt.ask("Shell I run the command for you?", choices=["y", "n"])
    if response == "y":
        console.print(f"Running: '{last_action.revert_command}'", style=Style(color="red"))
        os.system(last_action.revert_command)
    if response == "n":
        console.print("Ok, Bye!", style=Style(color="green"))
