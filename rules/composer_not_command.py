import re
from utils import replace_argument, for_app


@for_app('composer')
def match(command):
    return (('did you mean this?' in command.output.lower()
             or 'did you mean one of these?' in command.output.lower())) or (
        "install" in command.script_parts and "composer require" in command.output.lower()
    )


def get_new_command(command):
    if "install" in command.script_parts and "composer require" in command.output.lower():
        return replace_argument(command, "install", "require")
    
    broken_matches = re.findall(r'Command "([^"]*)"', command.output)
    if not broken_matches:
        return command.script

    suggested_matches = re.findall(
        r'Did you mean (this|one of these)\?[^\n]*\n\s*([^\n]*)',
        command.output, re.IGNORECASE)

    if not suggested_matches:
        return command.script

    broken_cmd = broken_matches[0]
    new_cmd = suggested_matches[0][1].strip()

    return replace_argument(command, broken_cmd, new_cmd)

'''
$ composer instll
Command "instll" is not defined. Did you mean this?
    install

oops -> $ composer install
'''