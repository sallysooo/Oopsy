import re
from utils import for_app

@for_app("git")
def match(command):
    return "push" in command.script and "The upstream branch of your current branch does not match" in command.output


def get_new_command(command):
    return re.findall(r'^ +(git push [^\s]+ [^\s]+)', command.output, re.MULTILINE)[0]
