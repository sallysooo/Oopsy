from utils import sudo_support
from shutil import which

WHITELIST = {
    'docker-compose',
    'apt-key',
    'pip-download',
    'npm-run',
    'kubectl-create',  
    # add more...
}

@sudo_support
def match(command):
    parts = command.script_parts
    if not parts: return False
    first_part = parts[0]
    
    if first_part in WHITELIST:
        return False
    if "-" not in first_part:
        return False
    if which(first_part):
        return False

    cmd = first_part.split("-")[0]
    return which(cmd) is not None

@sudo_support
def get_new_command(command):
    return command.script.replace("-", " ", 1)

'''
$ git-commit -m "msg"
oops -> $ git commit -m "msg"

$ docker-compose up
oops -> (it's in WHITELIST: no revision)
'''