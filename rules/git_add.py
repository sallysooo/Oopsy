import re
import os
from utils import shell_and, for_app

def _get_missing_file(command):
    pathspec = re.findall(
        r"error: pathspec '([^']*)' "
        r'did not match any file\(s\) known to git.', command.output)[0]
    if os.path.exists(pathspec):
        return pathspec
    return None

@for_app("git")
def match(command):
    return ('did not match any file(s) known to git.' in command.output
            and _get_missing_file(command) is not None)


def get_new_command(command):
    missing_file = _get_missing_file(command)
    return shell_and(f"git add -- {missing_file}", command.script)

'''
Git 명령 중 빠뜨린 파일을 자동으로 git add 해주는 명령 제안
$ git commit -m "initial"
error: pathspec 'main.py' did not match any file(s) known to git.

oops -> git add -- main.py && git commit -m "initial"
'''