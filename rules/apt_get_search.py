import re
from utils import for_app

@for_app('apt-get')
def match(command):
    return command.script.startswith('apt-get search')


def get_new_command(command):
    return re.sub(r'^apt-get', 'apt-cache', command.script)

'''
$ apt-get search git

oops -> $ apt-cache search git
'''