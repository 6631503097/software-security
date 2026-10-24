#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf 'Week 12 Cosign evidence | Wanna San | 6631503097 | The Imposters\n'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
python3 - "$1" <<'PY'
import json,pathlib,sys,shlex
r=pathlib.Path('submission/week12-6631503097/evidence/task3-signing');mode=sys.argv[1];s=json.loads((r/('sign-status.json' if mode=='sign' else 'verify-status.json')).read_text());print('\nExact executed command:\n'+shlex.join(s['command']));print('Exit:',s['exit_status']);print('Started:',s['started_utc']);print('Finished:',s['finished_utc'])
if mode=='sign':
 print('\nSanitized genuine signing output (authentication output excluded):');print((r/'sign.sanitized-output.txt').read_text())
else:
 print('\nGenuine verification output:');print((r/'verify.stderr.txt').read_text());print((r/'verify.stdout.json').read_text())
v=json.loads((r/'verified-result.json').read_text());print('\nActual certificate email:',v['actual_certificate_email']);print('Actual certificate OIDC issuer:',v['actual_certificate_oidc_issuer']);print('Exact identity and issuer match:',v['expected_identity_matches'] and v['expected_issuer_matches']);print('Approved digest verified:',v['verified_digest']);print('Transparency-log entries:',v['transparency_entry_count']);print('GHCR package visibility:',v['visibility']);print('Policy weakened:',v['policy_weakened'])
PY
