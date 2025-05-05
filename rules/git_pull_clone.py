from utils import replace_argument, for_app


@for_app("git")
def match(command):
    return ('fatal: Not a git repository' in command.output
            and "Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set)." in command.output)


def get_new_command(command):
    return replace_argument(command.script, 'pull', 'clone')
