import subprocess
import re
from utils import for_app, get_closest, replace_argument, sudo_support

@sudo_support
@for_app('apt', 'apt-get', 'apt-cache')
def match(command):
    return 'invalid operation' in command.output.lower()

def _get_available_operations(app):
    try:
        result = subprocess.run(
            [app, '--help'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        output = result.stdout
    except Exception:
        return []
    
    # extract commands from apt --help
    operations = []
    for line in output.splitlines():
        line = line.strip()
        if re.match(r'^[a-z\-]+\s', line):
            operations.append(line.split()[0])
    return list(set(operations)) # remove duplicates

@sudo_support
def get_new_command(command):
    app = command.script_parts[0]
    wrong_op = command.script_parts[1]
    operations = _get_available_operations(app)
    closest = get_closest(wrong_op, operations)
    
    if not closest:
        return command.script # fallback
    
    return replace_argument(command, wrong_op, closest)

'''
apt 관련 명령에서 잘못된 작업 이름을 입력했을 때 자동으로 올바른 명령어를 제안
$ sudo apt uninstall curl
E: Invalid operation uninstall

oops -> $ sudo apt remove curl
'''
