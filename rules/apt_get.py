from utils import sudo_support
from shutil import which
import subprocess

@sudo_support
def match(command):
    if ("not found" in command.output.lower()
        or "not installed" in command.output.lower()):
        executable = get_executable(command)
        return not which(executable) and get_package(executable) is not None
    return False

@sudo_support
def get_new_command(command):
    executable = get_executable(command)
    package = get_package(executable)
    return f"sudo apt-get install {package} && {command.script}"

def get_executable(command):
    '''if sudo: extract next word / else: extract first word'''
    parts = command.script_parts
    return parts[1] if parts[0] == "sudo" else parts[0]

def get_package(executable):
    '''infer the package name by Ubuntu's 'command-not-found' system'''
    try:
        output = subprocess.check_output(
            ['command-not-found', executable],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        # ex: "The program '<cmd>' is currently not installed. You can install it by typing:\nsudo apt install <package>"
        for line in output.split('\n'):
            if 'apt install' in line:
                parts = line.strip().split()
                if 'install' in parts:
                    idx = parts.index('install')
                    return parts[idx+1]
    except Exception:
        return None


# $ not_exist
# oops -> sudo apt install not_exist && not_exist