import re
from utils import for_app, shell_and

@for_app('docker')
def match(command):
    '''
    warning you that you need to remove a container before removing an image.
    '''
    return 'image is being used by running container' in command.output


def get_new_command(command):
    '''
    Prepends docker container rm -f {container ID} to
    the previous docker image rm {image ID} command
    '''
    container_id = re.findall(r'container\s+([a-f0-9]+)', command.output.lower())
    return shell_and(f'docker container rm -f {container_id}', command.script)

'''
$ docker rmi abc123
Error response from daemon: conflict: unable to remove repository reference "abc123" (must force) - image is being used by running container 456def

oops -> $ docker container rm -f 456def && docker rmi abc123
'''