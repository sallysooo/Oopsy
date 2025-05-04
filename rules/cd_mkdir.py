from utils import starts_with

def match(command):
    return(
        starts_with(command, "cd ")
        and "No such file or directory" in command.output
    )

def get_new_command(command):
    path = command.script_parts[1]
    return f"mkdir -p {path} && cd {path}"

# $ cd somenewdir
# oops -> mkdir -p somenewdir && cd somenewdir