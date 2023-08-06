<p align="center">
   <img src="https://xethub.com/xdssio/gitease/raw/branch/main/docs/images/logo.png" alt="logo" width="400" />
</p>

# GitEase
[![Version](https://img.shields.io/pypi/v/gitease.svg?style=flat)](https://pypi.python.org/pypi/gitease/)
[![Python](https://img.shields.io/pypi/pyversions/gitease.svg?style=flat)](https://pypi.python.org/pypi/gitease/)
[![License](https://img.shields.io/github/license/xetdata/gitease?style=flat)](https://xethub.com/xdssio/gitease/src/branch/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/gitease?style=flat)](https://pypi.python.org/pypi/gitease/)
[![Documentation Status](https://readthedocs.org/projects/gitease/badge/?version=latest)](https://gitease.readthedocs.io/en/latest/?badge=latest)


A tool to simplify git usage with sprinkles of AI magic.

Humans think in simpler terms than git operates in. This tool aims to bridge that gap by providing a simpler language to
do common git tasks. Plus an LLM can write your commit messages for you.

You can load recent information with `gs load`, save current changes with `gs save` and share them with `gs share`.    
Behind the scenes it's exactly what you would expect from git, but with a simpler interface.

## Install

* Get an [openai api key](https://platform.openai.com/account/api-keys)

```bash
$ export OPENAI_API_KEY=...
$ pip install gitease
```

* If OPENAI_API_KEY is not set, you will be prompted to enter a commit message manually.

## Usage

Within a repo, run:

```bash
$ ge --help

Commands:
  --help:  Show this message and exit.        
    save <message>: Add and commit files to git. Massage is generated if not provided         
    share <message>: Share to remote - Add, commit and push changes to git. Massage is generated if not provided
    load :  Pull recent updates from git
    message: Generate commit message from diff using AI.
    undo: Undo last git action - only works using AI
```
### Examples
```bash
$ ge save

> Entering new StuffDocumentsChain chain...


> Entering new LLMChain chain...
Prompt after formatting:
Write a concise summary of the following:
...
> Finished chain.

Your commit message is:
docs: Update documentation, configuration, and index files
This commit updates the documentation, configuration, and index files for the project, including Makefile,
conf.py, and index.rst. These changes provide information about the project, its features, and quickstart
instructions. Additionally, it updates the version of gitease from 0.0.5 to 0.0.6.

To confirm, press Enter.
Otherwise, write your own message:
Press CTRL+C to cancel
Response:
```

```bash
# Add and Commit all python files in src with the message "feat: Add new script"
ge save -a 'src/*.py' -m 'feat: Add new script'

# Add multiple files
ge save -a README.md -a gitease/cli.py

# Add and commits everything without prompting for validation
ge save -y

# Add the README.md file and commit with a generated message
ge share -a README.md -y 

# Pull recent changes from git
ge load
```

```bash
$ ge undo

Welcome to GitEase
Last git action is: Update README and CLI files
A revert command is: git reset HEAD@{0}
Shell I run the command for you? [y/n]: 
Running: git reset HEAD@{0}
Unstaged changes after reset:
M       README.md
M       gitease/cli.py
```