import re
from utils import replace_argument, for_app


@for_app("conda")
def match(command):
    return "Did you mean 'conda" in command.output

def get_new_command(command):
    matches = re.findall(r"'conda ([^']*)'", command.output)
    if len(matches) < 2:
        return command.script # fallback
    
    broken_cmd = matches[0]
    correct_cmd = matches[1]
    return replace_argument(command, broken_cmd, correct_cmd)

'''
$ conda instll numpy
CommandNotFoundError: No command 'conda instll'. Did you mean 'conda install'?

oops -> $ conda install numpy
'''