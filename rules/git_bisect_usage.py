import re
from utils import replace_argument, for_app

@for_app("git")
def match(command):
    return ('bisect' in command.script_parts and
            'usage: git bisect' in command.output)

def get_new_command(command):
    broken = re.findall(r'git bisect ([^ $]*).*', command.script)[0]
    usage = re.findall(r'usage: git bisect \[([^\]]+)\]', command.output)[0]
    return replace_argument(command, broken, usage.split('|'))
