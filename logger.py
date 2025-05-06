import datetime

LOGFILE = "oops.log"

def log_match(command, rule_name, fixed_command):
    with open(LOGFILE, "a") as f:
        f.write(f"[MATCH] {timestamp()} | Rule: {rule_name} | Input: '{command.script}' → Output: '{fixed_command}'\n")

def log_no_match(command):
    with open(LOGFILE, "a") as f:
        f.write(f"[NO MATCH] {timestamp()} | Input: '{command.script}' | Output: '{command.output[:100]}'\n")

def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")