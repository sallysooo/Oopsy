import re
from utils import shell_and

MISSING_MODULE = r"ModuleNotFoundError: No module named '([^']+)'"


def match(command):
    return "ModuleNotFoundError: No module named '" in command.output


def get_new_command(command):
    missing_module = re.findall(MISSING_MODULE, command.output)[0]
    return shell_and(f"pip install {missing_module}", command.script)
