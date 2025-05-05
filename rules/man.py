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


'''
def get_new_command(command):
    if '3' in command.script:
        return command.script.replace("3", "2")
    if '2' in command.script:
        return command.script.replace("2", "3")

    last_arg = command.script_parts[-1]
    help_command = last_arg + ' --help'

    # If there are no man pages for last_arg, suggest `last_arg --help` instead.
    # Otherwise, suggest `--help` after suggesting other man page sections.
    if command.output.strip() == 'No manual entry for ' + last_arg:
        return [help_command]

    split_cmd2 = command.script_parts
    split_cmd3 = split_cmd2[:]

    split_cmd2.insert(1, ' 2 ')
    split_cmd3.insert(1, ' 3 ')

    return [
        "".join(split_cmd3),
        "".join(split_cmd2),
        help_command,
    ]
'''