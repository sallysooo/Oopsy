# core logic (ex. load rule files dynamically)
import os
import importlib # load module dynamically

def load_rules():
    rules = []
    rules_dir = os.path.join(os.path.dirname(__file__), 'rules') # paste 'rules' directory under current file location
    for file in os.listdir(rules_dir):
        if file.endswith('.py') and not file.startswith('__'): # git_branch.py
            mod_name = f"rules.{file[:-3]}" # rules.git_branch
            mod = importlib.import_module(mod_name) # import rules.git_branch
            rules.append(mod)
    return rules


