from utils import for_app, quote

def match(command):
    return for_app("grep")(command) and "No such file or directory" in command.output

def get_new_command(command):
    parts = command.script_parts
    if len(parts) >= 3:
        return f"{parts[0]} {quote(parts[1])} {parts[2]}"
    return command.script

# $grep hello myfile.txt
# oops -> $ grep "hello" myfile.txt