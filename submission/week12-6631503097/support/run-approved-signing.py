import pathlib,subprocess,json,datetime,re,hashlib,urllib.request,urllib.error
root=pathlib.Path(__file__).resolve().parents[1];e=root/'evidence/task3-signing';e.mkdir(exist_ok=True)
policy=json.loads((root/'preparation/ghcr-signing-20261024/expected-signer-policy.json').read_text());ref=policy['image'];binary='/private/tmp/week12-tools/cosign/v3.1.4/cosign';assert hashlib.sha256(pathlib.Path(binary).read_bytes()).hexdigest()=='9f9b8cd557cf2e5b3df3373a00baa005a86b02391e3e06dd0ce37b3a1533d3a4'
p=subprocess.run(['/Applications/Docker.app/Contents/Resources/bin/docker-credential-desktop','get'],input='ghcr.io\n',capture_output=True,text=True,timeout=20);assert p.returncode==0;c=json.loads(p.stdout);req=urllib.request.Request('https://api.github.com/users/6631503097/packages/container/week12-supplychain',headers={'Authorization':'Bearer '+c['Secret'],'Accept':'application/vnd.github+json','User-Agent':'Week12-authorized-signing'})
with urllib.request.urlopen(req,timeout=30) as response:data=json.load(response);assert data['visibility']=='private'
(e/'pre-sign-visibility.json').write_text(json.dumps({'visibility':'private','http_status':200,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n');c=None
cmd=[binary,'sign','--yes','--fulcio-auth-flow','normal','--oidc-disable-ambient-providers','--bundle',str(e/'image.sigstore.json'),ref]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();(e/'sign-command.json').write_text(json.dumps({'command':cmd,'authorization':'Explicit student approval for exact recorded digest, GitHub OIDC, email and public log; --yes applies only that already-given consent. normal forces browser flow.','expected_identity':policy['certificate_identity'],'expected_issuer':policy['certificate_oidc_issuer'],'started_utc':start},indent=2)+'\n')
print('Authorized keyless signing is starting. Complete GitHub login/2FA in your browser.',flush=True)
p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
with (e/'sign.sanitized-output.txt').open('w') as log:
 log.write('Authentication URLs/codes/tokens and unrecognized lines excluded before display or persistence. stdout/stderr merged; only safe tool progress retained.\n')
 for raw in p.stdout:
  line=re.sub(r'\x1b\[[0-9;]*m','',raw.rstrip())
  safe=any(line.startswith(prefix) for prefix in ['Generating ephemeral keys','Retrieving signed certificate','Successfully verified SCT','tlog entry created','Pushing signature','Wrote','Signing artifact'])
  if safe and not re.search(r'https?://|token|code=|eyJ[A-Za-z0-9_-]+\.',line,re.I):
   print(line,flush=True);log.write(line+'\n');log.flush()
  elif line.startswith('Error:'):
   # Keep ordinary error text, excluding potentially credential-bearing URLs/JWTs.
   line=re.sub(r'https?://\S+','<URL omitted>',line);line=re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)?','<JWT omitted>',line)
   if re.search(r'token|authorization|secret|password|code=',line,re.I):line='Error: authentication-related error details omitted to protect credentials.'
   print(line,flush=True);log.write(line+'\n');log.flush()
rc=p.wait();record={'command':cmd,'exit_status':rc,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_authentication_output_saved':False};(e/'sign-status.json').write_text(json.dumps(record,indent=2)+'\n');print('Cosign signing exit status:',rc,flush=True)
