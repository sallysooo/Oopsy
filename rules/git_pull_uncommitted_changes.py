from utils import shell_and, for_app

@for_app("git")
def match(command):
    return (
        "pull" in command.script and
        any(keyword in command.output.lower() for keyword in [
            "you have unstaged changes",
            "contains uncommitted changes",
            "would be overwritten by merge"
        ])
    )

def get_new_command(command):
    return shell_and("git stash", "git pull", "git stash pop")

'''
로컬에 변경사항이 있을 때 git pull 실패하는 경우 stash 기반 해결 제안하기
$ git pull
error: Your local changes to the following files would be overwritten by merge

oops -> git stash && git pull && git stash pop
'''