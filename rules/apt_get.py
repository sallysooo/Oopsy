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

'''
from types import ModuleType
from thefuck.specific.apt import apt_available
from thefuck.utils import memoize, which
from thefuck.shells import shell

try:
    from CommandNotFound import CommandNotFound

    enabled_by_default = apt_available

    if isinstance(CommandNotFound, ModuleType):
        # For ubuntu 18.04+
        _get_packages = CommandNotFound.CommandNotFound().get_packages
    else:
        # For older versions
        _get_packages = CommandNotFound().getPackages
except ImportError:
    enabled_by_default = False


def _get_executable(command):
    if command.script_parts[0] == 'sudo':
        return command.script_parts[1]
    else:
        return command.script_parts[0]


@memoize
def get_package(executable):
    try:
        packages = _get_packages(executable)
        return packages[0][0]
    except IndexError:
        # IndexError is thrown when no matching package is found
        return None


def match(command):
    if 'not found' in command.output or 'not installed' in command.output:
        executable = _get_executable(command)
        return not which(executable) and get_package(executable)
    else:
        return False


def get_new_command(command):
    executable = _get_executable(command)
    name = get_package(executable)
    formatme = shell.and_('sudo apt-get install {}', '{}')
    return formatme.format(name, command.script)
'''