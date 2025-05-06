from shutil import which
import os

def _get_executable_prefix(word):
    """입력된 단어가 어떤 명령어로 시작하는지 찾기"""
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for dir in paths:
        try:
            for f in os.listdir(dir):
                if word.startswith(f) and which(f):
                    return f
        except FileNotFoundError:
            continue
    return None

def match(command):
    first = command.script_parts[0]
    return which(first) is None and _get_executable_prefix(first) is not None

def get_new_command(command):
    first = command.script_parts[0]
    exe = _get_executable_prefix(first)
    return command.script.replace(exe, f"{exe} ", 1)

'''
shutil.which() + os.listdir($PATH) 기반으로 prefix 탐색

$ gitcommit -m "msg"

oops -> $ git commit -m "msg"
'''