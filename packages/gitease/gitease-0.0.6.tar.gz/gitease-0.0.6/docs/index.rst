.. image:: https://xethub.com/xdssio/gitease/raw/branch/main/docs/images/logo.png
  :width: 250
  :alt: gitease-logo


Welcome to GitEase's documentation!
===================================

A tool to simplify Git usage with sprinkles of AI magic.


Not every code change is momentous; for a quick fix, a sole contributor or a toy example, GitEase is a simplified way to run git tasks. Save, load and share is how people think, and for the heavy mental load of a commit message or the undo command? AI can do that for you.

Features
==================

GitEase provides a mental wrapper around basic git operations.

- **ge load** - loads recent updates (git pull)
- **ge save** - saves current changes (git add, commit and generate a commit message)
- **ge share** - shares changes to remote by adding, committing, and pushing changes to git
- **ge message** - generates commit message from diff using AI
- **get undo** - undo the latest git action using AI


Quickstart
==================
`pip install gitease`

If you want AI features:

1. Get an `openai api key <https://platform.openai.com/account/api-keys>`_ and set it up.
2. Set environment variable: `export OPENAI_API_KEY=...`

Examples
==================

.. code-block:: bash

   ge save

   > Entering new StuffDocumentsChain chain...


   > Entering new LLMChain chain...
   Prompt after formatting:
   Write a concise summary of the following:
   ...
   > Finished chain.
   Automated commit - 4 files:
    writing README.md new instructions.
   gitease/__init__.py
   gitease/cli.py
   gitease/git_helper.py
   pyproject.toml

    To confirm, press Enter.
    Otherwise, write your own message:
    Press CTRL+C to cancel
    Response:


.. code-block:: bash

   $ ge undo

   Welcome to GitEase
   Last git action is: Update README and CLI files
   A revert command is: git reset HEAD@{0}
   Shell I run the command for you? [y/n]:
   Running: git reset HEAD@{0}
   Unstaged changes after reset:
   M       README.md
   M       gitease/cli.py


---------------------------------------

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   markdowns/quickstart
   markdowns/usage