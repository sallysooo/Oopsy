from utils import replace_argument, for_app


@for_app('php')
def match(command):
    return ('-s' in command.script_parts
            and command.script_parts[-1] != '-s')


def get_new_command(command):
    return replace_argument(command.script, "-s", "-S")
