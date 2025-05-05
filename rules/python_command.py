# add 'python' suffix to the command if
#  1) The script does not have execute permission or
#  2) is interpreted as shell script

def match(command):
    return (command.script_parts
            and command.script_parts[0].endswith('.py')
            and ('Permission denied' in command.output or
                 'command not found' in command.output))

def get_new_command(command):
    return 'python ' + command.script
