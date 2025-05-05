import re
from utils import for_app, shell_and


@for_app('touch')
def match(command):
    return 'No such file or directory' in command.output


def get_new_command(command):
    path = re.findall(
        r"touch: (?:cannot touch ')?(.+)/.+'?:", command.output)[0]
    return shell_and(u'mkdir -p {path}', command.script)
