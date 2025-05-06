
def for_app(*app_names):
    '''여러 앱 이름을 받아서, 첫 번째 명령어가 그 중 하나인지 확인'''
    def decorator(match_func):
        def wrapper(command):
            if hasattr(command, 'script_parts') and command.script_parts:
                if command.script_parts[0] in app_names:
                    return match_func(command)
            return False
        return wrapper
    return decorator

def replace_argument(command, old, new):
    '''스크립트 내에서 인자를 교체'''
    parts = command.script_parts
    try:
        index = parts.index(old)
        parts[index] = new
        return ' '.join(parts)
    except ValueError:
        return command.script

def get_closest(command_name, possibilities):
    '''가장 유사한 명령어를 반환'''
    from difflib import get_close_matches
    matches = get_close_matches(command_name, possibilities, n=1)
    return matches[0] if matches else None

def starts_with(command, text):
    '''스크립트가 특정 문자열로 시작하는지 확인'''
    return command.script.strip().startswith(text)

def ends_with(command, text):
    '''스크립트가 특정 문자열로 끝나는지 확인'''
    return command.script.strip().endswith(text)

def contains(command, text):
    '''스크립트 내에 특정 텍스트 포함 여부 확인'''
    return text in command.script

def sudo_support(fn):
    '''sudo가 있는 명령도 처리할 수 있게 매핑'''
    def wrapper(command, *args, **kwargs):
        if command.script.startswith("sudo "):
            stripped = command.script[5:]
            cmd = type(command)(stripped, command.output)
            return fn(cmd, *args, **kwargs)
        return fn(command, *args, **kwargs)
    return wrapper

def append_argument(command, new_arg):
    """명령어에 인자를 추가"""
    return command.script + ' ' + new_arg


def remove_argument(command, arg):
    """특정 인자를 제거"""
    parts = command.script_parts
    parts = [p for p in parts if p != arg]
    return ' '.join(parts)


def quote(s):
    """공백 포함 문자열을 따옴표로 감싸기"""
    if ' ' in s:
        return f'"{s}"'
    return s

def shell_and(*cmds):
    '''두 명령어를 &&로 연결'''
    return " && ".join(cmds)

