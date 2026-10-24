#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf 'Week 12 Task 3 | Wanna San | 6631503097 | The Imposters\n'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
printf '\nPreserved genuine build result:\n'
python3 - <<'PY'
import json,pathlib,shlex
r=pathlib.Path('submission/week12-6631503097/evidence/task3');b=json.loads((r/'build-status.json').read_text());i=json.loads((r/'image-inspect.json').read_text())[0]
print('Command:',shlex.join(b['command']));print('CWD:',b['cwd']);print('Exit:',b['exit_status']);print('Platform:',i['Os']+'/'+i['Architecture']);print('Image ID:',i['Id']);print('Tags:',i['RepoTags'])
PY
printf '\n$ tail -15 evidence/task3/build.stderr.txt\n'
tail -15 submission/week12-6631503097/evidence/task3/build.stderr.txt
printf '\nWarning in full build log: pip ran as root inside the disposable build image.\nNo image publication occurred; naming to docker.io is a local tag.\n'
