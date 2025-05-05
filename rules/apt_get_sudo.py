from utils import starts_with

def match(command):
    return(
        starts_with(command, "apt-get") or starts_with(command, "apt")
    ) and "permission denied" in command.output.lower()

def get_new_command(command):
    return f"sudo {command.script}"

# $ apt install foo
# oops -> sudo apt install foo