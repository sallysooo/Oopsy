from utils import for_app, shell_and, quote


tar_extensions = ('.tar', '.tar.Z', '.tar.bz2', '.tar.gz', '.tar.lz',
                  '.tar.lzma', '.tar.xz', '.taz', '.tb2', '.tbz', '.tbz2',
                  '.tgz', '.tlz', '.txz', '.tz')


def _is_tar_extract(cmd_str):
    if '--extract' in cmd_str:
        return True
    parts = cmd_str.split()
    return len(parts) > 1 and 'x' in parts[1]


def _tar_file(parts):
    for part in parts:
        for ext in tar_extensions:
            if part.endswith(ext):
                return (part, part[:-len(ext)])
    return None


@for_app('tar')
def match(command):
    return ('-C' not in command.script
            and _is_tar_extract(command.script)
            and _tar_file(command.script_parts) is not None)


def get_new_command(command):
    tar_file, dest_dir = _tar_file(command.script_parts)
    dest_dir = quote(dest_dir)
    return shell_and(f'mkdir -p {dest_dir}', f'{command.script} -C {dest_dir}')

'''
$ tar xf logs.tar.gz -> All the files in current directory gets untarred randomly

oops -> mkdir -p logs && tar xf logs.tar.gz -C logs
'''