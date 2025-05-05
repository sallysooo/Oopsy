import re
import os
from utils import shell_and, quote


# extract <file> and <line> from various error messages
patterns = [
    r'File "(?P<file>[^"]+)", line (?P<line>\d+)',           # Python
    r'(?P<file>[^:\n]+): line (?P<line>\d+)',                # Shell(bash, sh, ssh)
    r'(?P<file>[^:\n]+):(?P<line>\d+):(?P<col>\d+)?',        # C/C++, go, rustc, cargo
    r'at (?P<file>[^\s]+) line (?P<line>\d+)',               # Perl
]

compiled_patterns = [re.compile(p) for p in patterns]


def _extract_file_and_line(output):
    for pattern in compiled_patterns:
        match = pattern.search(output)
        if match:
            file = match.group("file")
            line = match.group("line")
            if os.path.isfile(file):
                return file, line
    return None, None


def match(command):
    return _extract_file_and_line(command.output)[0] is not None and 'EDITOR' in os.environ


def get_new_command(command):
    file, line = _extract_file_and_line(command.output)
    editor = os.environ['EDITOR']
    return shell_and(f'{editor} {quote(file)} +{line}', command.script)
    

'''
오류 메시지에 "file:line" 정보가 포함되어 있을 경우 -> 해당 파일의 특정 라인을 에디터로 열어주는 명령어 생성
$ python script.py
Traceback (most recent call last):
  File "main.py", line 42, in <module>
    ...
NameError: name 'x' is not defined


oops -> $ vim main.py +42 && python script.py
'''
