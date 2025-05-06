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
    '''
    #0. non-interactive method
    try:
        history_cmd = "HISTTIMEFORMAT='' history 1 | sed 's/^[ 0-9]*//'"
        last_cmd = subprocess.getoutput(history_cmd)
        if "oopsy.py" in last_cmd:
            history_cmd = "HISTTIMEFORMAT='' history 2 | head -1 | sed 's/^[0-9]*//'"
            last_cmd = subprocess.getoutput(history_cmd)
        return last_cmd
    except Exception as e:
        print(f"Failed to bring history: {e}")
        return
    '''
    #1. bring history from bash interactive mode
    bash_path = subprocess.getoutput('which bash')
    if os.path.exists(bash_path):
        try:
            out = subprocess.check_output(
                [bash_path, '-i', '-c', 'history -1'],
                stderr=subprocecss.DEVNULL,
                text=True
            ).strip().splitlines()
            
            if len(out) >= 2:
                return out[0].split(' ', 1)[-1] # 'abcde ls -l' -> 'ls -l'
        except Exception:
            pass
    
    #2. directly read bash history file
    bash_hist = os.path.expanduser('~/.bash_history')
    if os.path.exists(bash_hist):
        try:
            with open(bash_hist, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    return lines[-2].strip()
                elif lines:
                    return lines[-1].strip()
        except Exception:
            pass
    
    return ""


def main():
    last_cmd = get_last_command()
    print(f"last command: {last_cmd}")
    result = subprocess.getoutput(last_cmd)
    print(f"command output: {result[:50]}...")
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
                        return
                subprocess.call(new_cmd, shell=True)
                return
        except Exception as e:
            print(f"[ERROR] Rule {rule_name} : {e}")
    
    if config["log_enabled"]:
        log_no_match(cmd)
        
    print("No rules to apply...")

if __name__ == "__main__":
    main()




