import re
from utils import replace_argument

def match(command):
    return ('merge' in command.script
            and ' - not something we can merge' in command.output
            and 'Did you mean this?' in command.output)


def get_new_command(command):
    unknown_branch = re.findall(r'merge: (.+) - not something we can merge', command.output)[0]
    remote_branch = re.findall(r'Did you mean this\?\n\t([^\n]+)', command.output)[0]

    return replace_argument(command.script, unknown_branch, remote_branch)
