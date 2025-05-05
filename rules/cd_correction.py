"""Attempts to spellcheck and correct failed cd commands"""
import os
import six
from utils import for_app
from difflib import get_close_matches

MAX_ALLOWED_DIFF = 0.6


def _get_sub_dirs(parent):
    """Return only subdirectories under given path"""
    try:
        return [child for child in os.listdir(parent) if os.path.isdir(os.path.join(parent, child))]
    except Exception:
        return []
    

@for_app('cd')
def match(command):
    """Match function copied from cd_mkdir.py"""
    return (
        command.script.startswith('cd ') and any(msg in command.output.lower() for msg in [
            'no such file or directory',
            'cd: can\'t cd to',
            'does not exist'
        ])
    )


def get_new_command(command):
    """
    Attempt to rebuild the path string by spellchecking the directories.
    If it fails (i.e. no directories are a close enough match), then it
    defaults to the rules of cd_mkdir.
    Change sensitivity by changing MAX_ALLOWED_DIFF. Default value is 0.6
    """
    path = command.script_parts[1].split(os.sep)
    if path[-1] == '':
        path = path[:-1]

    if path[0] == '':
        cwd = os.sep
        path = path[1:]
    elif six.PY2:
        cwd = os.getcwdu()
    else:
        cwd = os.getcwd()
    
    for directory in path:
        if directory == ".":
            continue
        elif directory == "..":
            cwd = os.path.split(cwd)[0]
            continue
        
        best_matches = get_close_matches(directory, _get_sub_dirs(cwd), cutoff=MAX_ALLOWED_DIFF)
        if best_matches:
            cwd = os.path.join(cwd, best_matches[0])
        else:
            return command.script # fallback
    return f'cd "{cwd}"'

# $ cd my_prooject/
# >>> bash: cd: my_prooject/: No such file or directory

# oops -> $ cd my_project