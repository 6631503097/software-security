#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf '%s\n' 'Week 12 Task 1 | Wanna San | 6631503097 | The Imposters' 'Preserved genuine Trivy scan output (excerpt); full stdout/stderr saved separately.'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
printf '\n$ sed -n '\''15,40p'\'' evidence/task1/sca_scan.stdout.txt\n'
sed -n '15,40p' submission/week12-6631503097/evidence/task1/sca_scan.stdout.txt
printf '\nReal statuses: Trivy=0; pip-audit=1 (vulnerabilities found); image inspect=1 (not built); script=0 (masks statuses).\n'
