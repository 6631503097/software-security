#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf '%s\n' 'Week 12 Task 0 | Wanna San | The Imposters | Student 6631503097'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
printf '\n$ git branch --show-current; git rev-parse --short HEAD\n'
git branch --show-current; git rev-parse --short HEAD
printf '\n$ cat labs/week12-supply-chain/requirements.txt\n'
cat labs/week12-supply-chain/requirements.txt
printf '\nMapping: OWASP A03:2025; CWE-1104 (stale components), CWE-1395 (known-vulnerable dependencies).\nNo scan finding inferred for a package solely because it is old.\n'
