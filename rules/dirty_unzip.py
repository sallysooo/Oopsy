import os
import zipfile
from utils import for_app, quote


def _is_bad_zip(file):
    try:
        with zipfile.ZipFile(file, 'r') as archive:
            return len(archive.namelist()) > 1
    except Exception:
        return False


def _zip_file(command):
    # unzip works that way:
    # unzip [-flags] file[.zip] [file(s) ...] [-x file(s) ...]
    #                ^          ^ files to unzip from the archive
    #                archive to unzip
    for c in command.script_parts[1:]:
        if not c.startswith('-'):
            if c.endswith('.zip'):
                return c
            else:
                return f"{c}.zip"
    return None


@for_app('unzip')
def match(command):
    if '-d' in command.script:
        return False

    zip_file = _zip_file(command)
    return zip_file and _is_bad_zip(zip_file)


def get_new_command(command):
    zip_file = _zip_file(command)
    return f"{command.output} -d {quote(zip_file[:-4])}" # 'abc.zip' -> 'abc'


'''
$ unzip data.zip

oops -> $ unzip data.zip -d data
'''