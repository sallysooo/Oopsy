# main CLI Intro
from core import load_rules
import subprocess

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
        if rule.match(cmd):
            new_cmd = rule.get_new_command(cmd)
            print(f"Oopsy! Will you fix as: '{new_cmd}' ?")
            confirm = input("(Enter or n)")
            if confirm.strip().lower() != 'n':
                subprocess.call(new_cmd, shell=True)
            return
    print("No rules to apply...")

if __name__ == "__main__":
    main()




