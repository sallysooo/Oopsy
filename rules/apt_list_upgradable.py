from utils import for_app, sudo_support

@sudo_support
@for_app('apt')
def match(command):
    return 'apt list --upgradable' in command.output


@sudo_support
def get_new_command(command):
    return 'apt list --upgradable'
