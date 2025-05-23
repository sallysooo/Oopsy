"""
The confusion in systemctl's param order is massive.
"""
from utils import for_app

@for_app('systemctl')
def match(command):
    # Catches "Unknown operation 'service'." when executing systemctl with
    # misordered arguments
    cmd = command.script_parts
    return (cmd and 'Unknown operation \'' in command.output and
            len(cmd) - cmd.index('systemctl') == 3)

def get_new_command(command):
    cmd = command.script_parts[:]
    cmd[-1], cmd[-2] = cmd[-2], cmd[-1]
    return ' '.join(cmd)
