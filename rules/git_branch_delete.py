from utils import replace_argument, for_app

@for_app("git")
def match(command):
    return ('branch -d' in command.script
            and 'If you are sure you want to delete it' in command.output)

def get_new_command(command):
    return replace_argument(command.script, '-d', '-D')
