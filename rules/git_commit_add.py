from utils import for_app, replace_argument

@for_app("git")
def match(command):
    return (
        "commit" in command.script_parts
        and "no changes added to commit" in command.output
    )

def get_new_command(command):
    for opt in ("-a", "-p"):
        yield replace_argument(command.script, "commit", "commit {}".format(opt))
