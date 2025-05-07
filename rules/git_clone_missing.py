import os
from urllib.parse import urlparse
from shutil import which

def is_git_url(text):
    return(
        text.startswith("http://") or
        text.startswith("https://") or
        text.startswith("git@") or
        text.startswith("ssh://")
    )


def match(command):
    # We want it to be a URL by itself
    if len(command.script_parts) != 1:
        return False
    
    url = command.script.strip()
    
    if which(url):
        return False
    
    if not any(x in command.output.lower() for x in [
        'no such file or directory',
        'not found',
        'is not recognised as'
    ]):
        return False
    
    return is_git_url(url)

def get_new_command(command):
    return f"git clone {command.script}"

'''
$ https://github.com/user/project.git
bash: https://github.com/user/project.git: No such file or directory

oops -> $ git clone https://github.com/user/project.git
'''