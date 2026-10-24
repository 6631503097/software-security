#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf 'Week 12 PRIVATE GHCR publication | Wanna San | 6631503097 | The Imposters\n'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
python3 - <<'PY'
import pathlib,json,shlex
r=pathlib.Path('submission/week12-6631503097/evidence/task3-publication');pre=json.loads((r/'prepush-check.json').read_text());v=json.loads((r/'registry-verification.json').read_text());vis=json.loads((r/'immediate-visibility.json').read_text())
print('\nLocal image ID verified:',pre['local_id'])
for name in ['tag','push']:
 d=json.loads((r/(name+'-status.json')).read_text());print('$',shlex.join(d['command']));print('Exit:',d['exit_status'])
print('\nPreserved genuine docker push output (last 14 lines):');print('\n'.join((r/'push.stdout.txt').read_text().splitlines()[-14:]));print('\nImmediate authenticated GitHub API result:',json.dumps(vis));print('\nIndependent registry manifest verification: HTTP',v['registry_http_status']);print('Registry header digest:',v['registry_header_digest']);print('Computed manifest SHA256:',v['computed_manifest_digest']);print('Matches verified local image:',v['matches_verified_local_image']);print('Immutable reference:',v['immutable_reference']);print('\nNo Cosign, OIDC, Sigstore entry, Git commit/push, or PR performed.')
PY
