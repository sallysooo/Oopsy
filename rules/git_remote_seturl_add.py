from utils import for_app, replace_argument

@for_app("git")
def match(command):
    return ('set-url' in command.script
            and 'fatal: No such remote' in command.output)


def get_new_command(command):
    return replace_argument(command.script, 'set-url', 'add')
