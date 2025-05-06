from utils import for_app

@for_app("man")
def match(command):
    return True

def get_new_command(command):
    parts = command.script_parts
    last_arg = parts[-1]
    
    help_command = last_arg + " --help"
    
    # output : "No manual entry for <command>"
    if command.output.strip() == f"No manual entry for {last_arg}":
        return [help_command]
    
    parts2 = parts[:]
    parts3 = parts[:]
    
    parts2.insert(1, "2")
    parts3.insert(1, "3")
    
    return [
        " ".join(parts2),
        " ".join(parts3),
        help_command,
    ]

# $ man foo
# oops -> 1. man 3 foo / 2. man 2 foo / 3. foo --help

