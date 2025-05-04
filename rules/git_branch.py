from utils import for_app

def match(command):
    return for_app("git")(command) and "did you mean 'branch'" in command.output

def get_new_command(command):
    return "git branch"

# $ git brnch
# oops -> git branch