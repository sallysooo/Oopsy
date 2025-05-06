# Opens URL's in the default web browser
#
# Example:
# > open github.com
# The file ~/github.com does not exist.
# Perhaps you meant 'http://github.com'?
#
from utils import shell_and, for_app


def is_url(command):
    return any(ext in command for ext in
               ['.com', '.net', '.org', '.io', '.edu', '.me', '.ly', 'www.'])


@for_app('open', 'xdg-open', 'gnome-open', 'kde-open')
def match(command):
    return (
        is_url(command.script) or
        ('The file ' in command.output and 'does not exist' in command.output)
    )

def get_new_command(command):
    if is_url(command.script):
        return command.script.replace('open ', 'open http://', 1)

    arg = command.script.split(' ', 1)[1]
    # 기본적으로 touch 방식만 추천 (단순화 ver.)
    return shell_and(f'touch {arg}', command.script)

'''
$ open github.com
The file ~/github.com does not exist.

oops -> $ open http://github.com 


$ open myfile.txt
The file myfile.txt does not exist.

oops -> $ touch myfile.txt && open myfile.txt
'''