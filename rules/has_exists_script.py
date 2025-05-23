import os
from utils import sudo_support


@sudo_support
def match(command):
    return command.script_parts and os.path.exists(command.script_parts[0]) \
        and 'command not found' in command.output


@sudo_support
def get_new_command(command):
    return u'./{}'.format(command.script)
