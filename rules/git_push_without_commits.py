import re
from utils import shell_and, for_app


@for_app("git")
def match(command):
    return bool(re.search(r"src refspec \w+ does not match any", command.output))


def get_new_command(command):
    return shell_and('git commit -m "Initial commit"', command.script)
