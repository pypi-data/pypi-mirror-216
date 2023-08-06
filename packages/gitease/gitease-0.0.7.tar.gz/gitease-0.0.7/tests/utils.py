import subprocess
import os

TEST_REPO = os.getenv('GITEASE_TEST_REPO', "https://github.com/xdssio/gitease-testing-repo.git")


def file_exists(working_dir: str, file_name: str):
    response = subprocess.run(f"cd {working_dir} && git cat-file -e HEAD:{file_name}",
                              shell=True,
                              stderr=subprocess.PIPE)
    if response.stderr:
        return False
    return True
