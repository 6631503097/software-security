#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf '%s\n' 'Week 12 Task 1 | Wanna San | 6631503097 | The Imposters' 'Preserved genuine pip-audit stdout; process exit 1 = vulnerabilities found.'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
printf '\n$ cat evidence/task1/1792825120559037000.stdout.txt\n'
cat submission/week12-6631503097/evidence/task1/1792825120559037000.stdout.txt
printf '\nActual tool version checks: Trivy 0.74.0; pip-audit 2.9.0; container Python 3.9.25.\n'
