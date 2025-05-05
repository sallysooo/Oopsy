from utils import shell_and, for_app

@for_app("git")
def match(command):
    return 'pull' in command.script and 'set-upstream' in command.output


def get_new_command(command):
    line = command.output.split('\n')[-3].strip()
    branch = line.split(' ')[-1]
    set_upstream = line.replace('<remote>', 'origin')\
                       .replace('<branch>', branch)
    return shell_and(set_upstream, command.script)
