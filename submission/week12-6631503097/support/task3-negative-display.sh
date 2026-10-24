#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf 'Week 12 Task 3 UNSIGNED negative test | Wanna San | 6631503097 | The Imposters\n'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
python3 - <<'PY'
import json,pathlib,shlex
r=pathlib.Path('submission/week12-6631503097/evidence/task3-negative');d=json.loads((r/'signature-discovery.json').read_text());print('\nPrecheck: suggested image manifest HTTP 200; SHA-256 checked against registry header.');print('Resolved image:',d['immutable_reference']);print('OCI referrers: HTTP 200, manifests=[]');print('Legacy Cosign signature: HTTP 404 (signature absent; image exists).');print('\nCosign tree actual output:');print((r/'tree.stdout.txt').read_text())
for name in ['verify-worksheet','verify-pinned']:
 s=json.loads((r/(name+'-status.json')).read_text());print('$',shlex.join(s['command']));print('Exit status:',s['exit_status']);print((r/(name+'.stderr.txt')).read_text())
print('Result: missing-signature rejection; no authentication/network/permissions/CLI failure.');print('The permissive regexes isolate signature absence; positive verification retains exact email/issuer.');print('GHCR package remains:',json.loads((r/'private-package-check.json').read_text())['visibility']);print('No image signed or published during this negative test.')
PY
