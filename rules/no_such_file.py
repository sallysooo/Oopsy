import re
from utils import shell_and


patterns = (
    r"mv: cannot move '[^']*' to '([^']*)': No such file or directory",
    r"mv: cannot move '[^']*' to '([^']*)': Not a directory",
    r"cp: cannot create regular file '([^']*)': No such file or directory",
    r"cp: cannot create regular file '([^']*)': Not a directory",
)


def match(command):
    for pattern in patterns:
        if re.search(pattern, command.output):
            return True

    return False


def get_new_command(command):
    for pattern in patterns:
        file = re.findall(pattern, command.output)

        if file:
            file = file[0]
            dir = file[0:file.rfind('/')]

            formatme = shell_and('mkdir -p {}', '{}')
            return formatme.format(dir, command.script)
