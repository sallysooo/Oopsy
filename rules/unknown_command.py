import re
from utils import replace_argument


def match(command):
    return (re.search(r"([^:]*): Unknown command.*", command.output) is not None
            and re.search(r"Did you mean ([^?]*)?", command.output) is not None)


def get_new_command(command):
    broken_cmd = re.findall(r"([^:]*): Unknown command.*", command.output)[0]
    matched = re.findall(r"Did you mean ([^?]*)?", command.output)
    return replace_argument(command, broken_cmd, matched)
