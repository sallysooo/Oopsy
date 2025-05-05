# -*- encoding: utf-8 -*-
import re

def match(command):
    return ('command not found' in command.output.lower()
            and u' ' in command.script)

def get_new_command(command):
    return re.sub(u' ', ' ', command.script)
