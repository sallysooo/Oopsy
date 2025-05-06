import re
from utils import for_app

@for_app("git")
def match(command):
    return "remote delete" in command.script


def get_new_command(command):
    return re.sub(r"delete", "remove", command.script, 1)
