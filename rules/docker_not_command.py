import re
from utils import replace_argument, for_app, get_closest

DOCKER_COMMANDS = [
    "run", "build", "pull", "push", "start", "stop", "ps", "exec",
    "rm", "rmi", "images", "logs", "inspect", "compose", "volume",
    "container", "network", "login", "logout", "tag", "info"
]

@for_app('docker')
def match(command):
    return ('is not a docker command' in command.output.lower() 
            or 'usage:' in command.output.lower())

def get_new_command(command):
    wrong_cmd_match = re.findall(r"docker: '(\w+)' is not a docker command", command.output)
    if wrong_cmd_match:
        wrong_cmd = wrong_cmd_match[0]
        closest = get_closest(wrong_cmd, DOCKER_COMMANDS)
        if closest:
            return replace_argument(command, wrong_cmd, closest)
    return command.script

'''
docker 명령어 오타를 자동 수정해줌 : 오류 메시지에서 잘못된 명령어를 추출하여 유사도 기반으로 교정 제안
$ docker psx
docker: 'psx' is not a docker command.

oops -> $ docker ps
'''