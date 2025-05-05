import re
from utils import for_app

@for_app('cp')
def match(command):
    output = command.output.lower()
    return 'omitting directory' in output or 'is a directory' in output

def get_new_command(command):
    return re.sub(r'^cp', 'cp -a', command.script)

'''
$ cp mydir dest/
cp: -r not specified; omitting directory 'mydir'

oops -> $ cp -a mydir dest/

-a is similar as -dR --preserve=all
'''