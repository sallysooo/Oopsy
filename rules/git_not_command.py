import re
from utils import for_app, replace_argument, get_closest

@for_app("git")
def match(command):
    return (
        "is not a git command" in command.output.lower() and
        ("did you mean" in command.output.lower() or "most similar command" in command.output.lower())
    )

def get_new_command(command):
    broken_cmd = re.findall(r"git: '([^']*)' is not a git command", command.output)
    suggestion = re.findall(r'\n\s*([a-z][a-z0-9\-]+)\s*$', command.output.lower(), re.MULTILINE)

    if not broken_cmd or not suggestion:
        return command.script

    return replace_argument(command, broken_cmd[0], suggestion[0])

'''
$ git comit -m "msg"
git: 'comit' is not a git command. See 'git --help'.
Did you mean this?
        commit

oops -> $ git commit -m "msg"
'''