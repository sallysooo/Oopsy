import os
from utils import shell_and

def match(command):
    return (command.script.startswith('./')
            and 'permission denied' in command.output.lower()
            and os.path.exists(command.script_parts[0])
            and not os.access(command.script_parts[0], os.X_OK))


def get_new_command(command):
    filepath = command.script_parts[0][2:] # './my_script' -> 'my_script'
    return shell_and(f'chmod +x {filepath}', command.script)
    
'''
$ ./run_me
bash: ./run_me: Permission denied
oops -> $ chmod +x run_me && ./run_me
'''