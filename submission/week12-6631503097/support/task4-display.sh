#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf 'Week 12 Task 4 defenses | Wanna San | 6631503097 | The Imposters\n'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
python3 - "$1" <<'PY'
import json,pathlib,sys,shlex
root=pathlib.Path('submission/week12-6631503097');r=root/'evidence/task4'
if sys.argv[1]=='hash':
 print('\nActual disposable environment:',(r/'pip-version.stdout.txt').read_text().strip());print('PIP_CONFIG_FILE=/dev/null; inherited PIP_* settings removed.')
 for name in ['hash-refusal','single-index-refusal']:
  s=json.loads((r/(name+'-status.json')).read_text());print('\n$',shlex.join(s['command']));print('Exit:',s['exit_status']);print((r/(name+'.stdout.txt')).read_text());print((r/(name+'.stderr.txt')).read_text())
 print('Installed afterward:',(r/'installed-after.stdout.txt').read_text());print('No lab dependencies installed. Original requirements.txt unchanged.');print('\nClean pip configuration check:');print((r/'single-index-config.stdout.txt').read_text())
else:
 print('\nActual gate command: bash submission/week12-6631503097/support/task4-verification-gate.sh');print('Gate source (read-only; deploy is simulated):');print((root/'support/task4-verification-gate.sh').read_text());print('Actual gate exit:',json.loads((r/'gate-status.json').read_text())['exit_status']);print((r/'gate.stderr.txt').read_text());print('\n'.join((r/'gate.stdout.txt').read_text().splitlines()[-3:]));d=json.loads((r/'signature-provenance-distinction.json').read_text());print('\nActual signed predicate:',d['observed_signature_predicate_type']);print('SLSA provenance policy verified:',d['full_slsa_build_provenance_policy_verified']);print('No SLSA level claimed. No deployment, signing or publication executed.')
PY
