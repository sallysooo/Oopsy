def match(command):
    return "git: 'brnch' is not a git command" in command.output

def get_new_command(command):
    return command.script.replace("brnch", "branch")