# main CLI Intro
from core import load_rules
from logger import log_match, log_no_match
from config import load_config
import subprocess
import os

config = load_config()

class Command:
    def __init__(self, script, output):
        self.script = script
        self.output = output
    
    @property
    def script_parts(self):
        return self.script.strip().split()

    @property
    def stderr(self):
        return self.output

def get_last_command():
    # Method 1. directly read bash history file
    try:
        # view 2 history commands with bash (current & previous)
        cmd = '''
        bash -c '
        HISTFILE=~/.bash_history    # history file
        HISTIGNORE="*"              # ignore exclusion of saving history
        set -o history              # activate history in non-interactive mode
        history -r                  # read history file again
        history 2                   # 2 recent commands
        '
        '''
        out = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip().split('\n')

        if len(out) >= 2:
            prev_cmd = out[0].split(' ', 1)[-1].strip()
            current_cmd = out[1].split(' ', 1)[-1].strip()

            if 'oopsy.py' in current_cmd:
                return prev_cmd
            else:
                return current_cmd
    except Exception as e:
        print(f"[DEBUG] Method1 failed: {str(e)[:50]}")

    # Method 2. Directly read .bash_history (backup)
    try:
        with open(os.path.expanduser('~/.bash_history'), 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            if len(lines) >= 2 and 'oopsy.py' in lines[-1]:
                return lines[-2]
            elif lines:
                return lines[-1]
    except Exception as e:
        print(f"[DEBUG] Method2 failed: {str(e)[:50]}")
    

    print("Failed to track history. Enter command:")
    return input("> ")


def main():
    last_cmd = get_last_command()
    print(f"last command: {last_cmd}") # Debug
    result = subprocess.getoutput(last_cmd)
    print(f"command output: {result[:50]}...") # Debug
    cmd = Command(last_cmd, result) # error analysis & recommend revision
    
    rules = load_rules()
    
    for rule in rules:
        rule_name = rule.__name__
        if config["enabled_rules"] and rule_name not in config["enabled_rules"]:
            continue
        
        try:
            if rule.match(cmd):
                new_cmd = rule.get_new_command(cmd)
                
                if config["log_enabled"]:
                    log_match(cmd, rule_name, new_cmd)
                
                print(f"Oopsy! Will you fix as: '{new_cmd}' ?")
                if not config["auto_mode"]:
                    confirm = input("(Enter or n)")
                    if confirm.strip().lower() != 'n':
                        subprocess.call(new_cmd, shell=True)
                        return
                else:
                    return
        except Exception as e:
            print(f"[ERROR] Rule {rule_name} : {e}")
    
    if config["log_enabled"]:
        log_no_match(cmd)
        
    print("No rules to apply...")

if __name__ == "__main__":
    main()

