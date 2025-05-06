import re
import os
import subprocess
from utils import replace_argument

patterns = [r'no such file or directory: (.*)$',
            r"cannot access '(.*)': No such file or directory",
            r': (.*): No such file or directory',
            r"can't cd to (.*)$"]


def _get_destination(output, script_parts):
    for pattern in patterns:
        found = re.findall(pattern, output.lower())
        if found and found[0] in script_parts:
            return found[0]
    return None

def _get_bash_history():
    try:
        return subprocess.getoutput('history').split('\n')
    except Exception:
        return []


def _get_all_absolute_paths_from_history():
    paths = set()

    for line in _get_bash_history():
        tokens = line.strip().split()
        for token in tokens[1:]:
            if token.startswith('/') or token.startswith('~'):
                clean = token.rstrip('/')
                expanded = os.path.expanduser(clean)
                if os.path.exists(expanded):
                    paths.add(token)
    return paths

def match(command):
    return _get_destination(command.output, command.script_parts) is not None


def get_new_command(command):
    dest = _get_destination(command.output, command.script_parts)
    candidates = _get_all_absolute_paths_from_history(command)
    for path in candidates:
        if path.endswith(dest):
            return replace_argument(command, dest, path)
    return command.script    



'''
경로를 오타로 잘못 입력한 경우, 이전에 입력했던 정확한 경로를 history에서 찾아 자동 추천
- 에러 메시지에서 경로 추출
- bash history 에서 절대경로 후보 추출
- 존재하는 경로와 비교하여 가장 유사한 추천 1개 제공 (가장 유사하거나 최근 명령)

$ cd ~/Dev/projec
cd: no such file or directory: ~/Dev/projec

oops -> $ cd ~/Dev/project
'''
