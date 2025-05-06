from utils import replace_argument, for_app

@for_app("git")
def match(command):
    return ('push' in command.script
            and '! [rejected]' in command.output
            and 'failed to push some refs to' in command.output
            and 'Updates were rejected because the tip of your current branch is behind' in command.output)

def get_new_command(command):
    return replace_argument(command.script, 'push', 'push --force-with-lease')


