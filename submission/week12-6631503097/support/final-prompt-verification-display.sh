#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf 'Week 12 Prompt Problem verification | Wanna San | 6631503097 | The Imposters\n'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
python3 - <<'PY'
import pathlib,json
r=pathlib.Path('submission/week12-6631503097/evidence/final-qa');d=json.loads((r/'gate-wrong-identity-status.json').read_text());print('\nNecessary missing verification: deny branch of the AI-assisted gate.');print('Original support/task4-verification-gate.sh unchanged.');print('Temporary fixture changes only expected identity to unauthorized-signer@example.invalid.');print('Exact command:',d['command']);print('Actual exit:',d['exit_status']);print((r/'gate-wrong-identity.stderr.txt').read_text());print('ALLOW printed:',d['stdout_contains_allow']);print('DENY printed:',d['stderr_contains_deny']);print('Deployment executed:',d['deployment_executed']);print('Earlier genuine positive gate result: evidence/task4/gate-status.json, exit 0.');print('This verifies wrong-signer rejection; it does not prove SLSA provenance.')
PY
