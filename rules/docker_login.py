from utils import for_app, shell_and

@for_app('docker')
def match(command):
    return ('docker' in command.script
            and "access denied" in command.output
            and "may require 'docker login'" in command.output)

def get_new_command(command):
    return shell_and('docker login', command.script)
