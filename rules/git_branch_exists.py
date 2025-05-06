import re
from utils import for_app, shell_and

@for_app("git")
def match(command):
    return ("fatal: A branch named '" in command.output
            and "' already exists." in command.output)

def get_new_command(command):
    branch_name = re.findall(
        r"fatal: A branch named '(.+)' already exists.", command.output)[0]
    branch_name = branch_name.replace("'", r"\'")
    new_command_templates = [['git branch -d {0}', 'git branch {0}'],
                             ['git branch -d {0}', 'git checkout -b {0}'],
                             ['git branch -D {0}', 'git branch {0}'],
                             ['git branch -D {0}', 'git checkout -b {0}'],
                             ['git checkout {0}']]
    for new_command_template in new_command_templates:
        yield shell_and(*new_command_template).format(branch_name)
