from utils import replace_argument, shell_and, for_app

@for_app("git")
def match(command):
    return ('push' in command.script and
            '! [rejected]' in command.output and
            'failed to push some refs to' in command.output and
            ('Updates were rejected because the tip of your'
             ' current branch is behind' in command.output or
             'Updates were rejected because the remote '
             'contains work that you do' in command.output))


def get_new_command(command):
    return shell_and(replace_argument(command.script, 'push', 'pull'), command.script)
