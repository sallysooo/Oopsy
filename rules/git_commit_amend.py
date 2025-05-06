def match(command):
    return ('commit' in command.script_parts)


def get_new_command(command):
    return 'git commit --amend'
