from utils import for_app, shell_and

@for_app("cp", "mv")
def match(command):
    return (
        "no such file or directory" in command.output.lower()
        or (
            command.output.lower().startswith("cp: directory")
            and command.output.rstrip().lower().endswith("does not exist")
        )
    )

def get_new_command(command):
    dest_path = command.script_parts[-1] # last argument(= target path)
    return shell_and(f"mkdir -p {dest_path}", command.script)

'''
$ cp test.txt folder/test.txt
cp: cannot create regular file 'folder/test.txt': No such file or directory

oops -> mkdir -p folder && cp test.txt folder/test.txt
'''
