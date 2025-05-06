from utils import replace_argument, for_app

@for_app("git")
def match(command):
    return ('add' in command.script_parts
            and 'Use -f if you really want to add them.' in command.output)

def get_new_command(command):
    return replace_argument(command.script, 'add', 'add --force')
