from utils import for_app

@for_app("git")
def match(command):
    return (' git clone ' in command.script
            and 'fatal: Too many arguments.' in command.output)

def get_new_command(command):
    return command.script.replace(' git clone ', ' ', 1)
