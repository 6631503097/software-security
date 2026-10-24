#!/bin/bash
cd /private/tmp/software-security-wk12
clear
printf 'Week 12 Task 3 SBOM | Wanna San | 6631503097 | The Imposters\n'
printf '%s\n' "printf '%s | %s | ' \"\$(whoami)\" '6631503097'; date '+%F %T %Z'"
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
python3 - <<'PY'
import json,pathlib,shlex
r=pathlib.Path('submission/week12-6631503097/evidence/task3');s=json.loads((r/'sbom-status.json').read_text());v=json.loads((r/'validation-summary.json').read_text());f=v['flask'][0]
print('\nActual SBOM generation command:\n'+shlex.join(s['command']));print('SBOM exit:',s['exit_status']);print('Artifact:',r/'sbom.cdx.json');print('SBOM SHA-256:',v['sbom_sha256']);print('Format:',v['bomFormat'],v['specVersion'],'Schema validation:',v['schema_validation'],'Errors:',len(v['validation_errors']));print('Components:',v['total_components'],v['component_types']);print('Package ecosystems:',v['purl_ecosystems']);print('SBOM image ID matches Docker inspect:',v['image_id_matches']);print('Image ID:',v['source_image_id']);print('\nFlask component:');print('Name:',f['name'],'Version:',f['version'],'Type:',f['type']);print('PURL / bom-ref:',f['purl']);print('License:',f['licenses'][0]['license']['id']);print('Reported component hashes:',f['hashes'])
for prop in f['properties']:print(prop['name']+': '+prop['value'])
print('\nIndependent network-disabled image read:');print((r/'installed-flask.stdout.txt').read_text());print('Initial schema-host HTTP 403 retained; official CycloneDX GitHub schema retry PASS.');print('Inventory generation does not assert vulnerability-free or signed provenance.')
PY
