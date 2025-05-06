# main CLI Intro
from core import load_rules
from logger import log_match, log_no_match
from config import load_config
import subprocess

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
    return subprocess.getoutput('fc -ln -1')

def main():
    last_cmd = get_last_command()
    result = subprocess.getoutput(last_cmd)
    cmd = Command(last_cmd, result) # error analysis & recommend revision
    
    for rule in load_rules():
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




