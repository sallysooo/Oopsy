from utils import shell_and, for_app

@for_app("git")
def match(command):
    # catches "git branch list" in place of "git branch"
    return (command.script_parts
            and command.script_parts[1:] == 'branch list'.split())

def get_new_command(command):
    return shell_and('git branch --delete list', 'git branch')
