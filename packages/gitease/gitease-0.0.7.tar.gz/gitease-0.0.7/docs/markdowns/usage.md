# Usage

Within a repo, run:

## Help

```bash

$ ge --help

Commands:
  --help:  Show this message and exit.        
    save <message>: Add and commit files to git. Massage is generated if not provided         
    share <message>: Share to remote - Add, commit and push changes to git. Massage is genereated if not provided
    load :  Pull recent updates from git
    message: Generate commit message from diff using AI.
    undo: Undo last git action - only works using AI
```

## Save

Add and commit files to git. Massage is generated if not provided.

```bash
 Usage: ge save [OPTIONS]                                                                                                                                                                                                    
                                                                                                                                                                                                                             
 Add and commit files to git.                                                                                                                                                                                                
                                                                                                                                                                                                                             
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --add      -a      TEXT  Files to add. All of not provided [default: None]                                                                                                                                                │
│ --message  -m      TEXT  commit message - If not provided, Generate by AI (given OPENAI_API_KEY is set) [default: None]                                                                                                   │
│ --quiet    -q            If True - Quiet the the LLM thoughts and other messages                                                                                                                                          │
│ --yes      -y            If True - Skips confirmation message                                                                                                                                                             │
│ --help                   Show this message and exit.                                                                                                                                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
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
ge add -a 'src/*.py' -m 'feat: Add new script'

# Add multiple files
ge add -a README.md -a gitease/cli.py

# Add and commits everything without prompting for validation
ge -y
```

## Share

Run `ge save` and then push to remote.

```bash
Usage: ge share [OPTIONS]                                                                                                                                                                                                   
                                                                                                                                                                                                                             
 Share to remote: add, commit and push to git                                                                                                                                                                                
                                                                                                                                                                                                                             
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --add      -a      TEXT  Files to add. All of not provided [default: None]                                                                                                                                                │
│ --message  -m      TEXT  commit message - If not provided, Generate by AI (given OPENAI_API_KEY is set) [default: None]                                                                                                   │
│ --quiet    -q            If True - Quiet the the LLM thoughts and other messages                                                                                                                                          │
│ --yes      -y            If True - Skips confirmation message                                                                                                                                                             │
│ --help                   Show this message and exit.                                                                                                                                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Example

```bash
ge share

Prompt after formatting:
Generate an clear and elaborate git commit message written in present tense for the following code diff with the given specifications below:
Your entire response will be passed directly into git commit.
Include a concise summary of the change from each file in the diff.
Pick one of the following titles:
...
Your commit message is:
feat: Add documentation, configuration, and index files, update version and add new script
This commit adds documentation, configuration, and index files to the project, including Makefile, conf.py, and index.rst. These files provide information about the project, its features, and quickstart instructions. 
Additionally, it updates the version of gitease from 0.0.4 to 0.0.5 and adds a new script 'ge' to the pyproject.toml file. Finally, it updates the prompt path in the LanguageModel class to use os.path.join for better 
portability.

To confirm, press Enter.
Otherwise, write your own message:
Press CTRL+C to cancel
Response: 
```

## load

A simple wrapper around git pull. Pulls recent updates from git.

```bash
$ ge load --help
```

## Undo

Use AI on the git reflog to find the last git action and suggest how to undo it.

```bash
$ ge undo --help
```

### Example

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

