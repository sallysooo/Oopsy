import re

def match(command):
    return ('mkdir' in command.script
            and 'No such file or directory' in command.output)

def get_new_command(command):
    return re.sub('\\bmkdir (.*)', 'mkdir -p \\1', command.script)
