from utils import for_app

def match(command):
    return (for_app("rm")(command)
            and 'is a directory' in command.output)

def get_new_command(command):
    return f"{command.script} -rf"

# $ rm somedir
# oops -> $ rm -rf somedir