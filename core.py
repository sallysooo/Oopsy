# core logic (ex. load rule files dynamically)
import os
import importlib # load module dynamically

def load_rules():
    rules = []
    rules_dir = os.path.join(os.path.dirname(__file__), 'rules') # paste 'rules' directory under current file location
    for file in os.listdir(rules_dir):
        if file.endswith('.py') and not file.startswith('__'): # git_branch.py
            mod_name = f"rules.{file[:-3]}" # rules.git_branch
            try:
                mod = importlib.import_module(mod_name) # import rules.git_branch
                # if match(), get_new_command() exists
                if hasattr(mod, "match") and hasattr(mod, "get_new_command"): 
                    rules.append(mod)
            except Exception as e:
                print(f"Failed to import {mod_name} : {e}")
    return rules
