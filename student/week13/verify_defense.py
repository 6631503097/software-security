#!/usr/bin/env python3
"""Wanna San / 6631503097. Local contract checks, not an AWS IAM simulator."""
import argparse,fnmatch,json,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parent

def validate_policy(policy):
    statements=policy['Statement']
    if len(statements)!=2: raise ValueError('expected two least-privilege statements')
    expected=json.loads((ROOT/'iam-policy.json').read_text())
    for statement in statements:
        if statement['Effect']!='Allow' or '*' in statement['Action']:raise ValueError('excess action grant')
        if statement['Resource']=='*':raise ValueError('unbounded resource grant')
    get=next(s for s in statements if s['Action']==['s3:GetObject'])
    listing=next(s for s in statements if s['Action']==['s3:ListBucket'])
    if get['Resource']!='arn:aws:s3:::lab-app-bucket/app/*':raise ValueError('wrong object scope')
    if listing['Resource']!='arn:aws:s3:::lab-app-bucket':raise ValueError('wrong bucket scope')
    if listing.get('Condition')!={'StringLike':{'s3:prefix':['app/*']}}:raise ValueError('missing prefix guard')

def local_allows(policy,action,resource,prefix=None):
    # This models ONLY this policy's Allow statements and StringLike/s3:prefix.
    # Real AWS also considers other policies, explicit denies, boundaries and SCPs.
    for s in policy['Statement']:
        if s['Effect']!='Allow':continue
        actions=s['Action'] if isinstance(s['Action'],list) else [s['Action']]
        if not any(fnmatch.fnmatchcase(action,a) for a in actions):continue
        if not fnmatch.fnmatchcase(resource,s['Resource']):continue
        condition=s.get('Condition')
        if condition and (prefix is None or not any(fnmatch.fnmatchcase(prefix,p) for p in condition['StringLike']['s3:prefix'])):continue
        return True
    return False

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--image');args=parser.parse_args()
    policy=json.loads((ROOT/'iam-policy.json').read_text());validate_policy(policy)
    cases=[('allowed object','s3:GetObject','arn:aws:s3:::lab-app-bucket/app/a',None,True),('other prefix','s3:GetObject','arn:aws:s3:::lab-app-bucket/private/a',None,False),('other bucket','s3:GetObject','arn:aws:s3:::other-bucket/app/a',None,False),('write blocked','s3:PutObject','arn:aws:s3:::lab-app-bucket/app/a',None,False),('delete blocked','s3:DeleteObject','arn:aws:s3:::lab-app-bucket/app/a',None,False),('IAM administration blocked','iam:CreateAccessKey','*',None,False),('list app','s3:ListBucket','arn:aws:s3:::lab-app-bucket','app/',True),('list other','s3:ListBucket','arn:aws:s3:::lab-app-bucket','private/',False),('list without prefix','s3:ListBucket','arn:aws:s3:::lab-app-bucket',None,False)]
    results=[]
    for name,action,resource,prefix,expected in cases:
        actual=local_allows(policy,action,resource,prefix)
        if actual!=expected:raise ValueError(name)
        results.append({'case':name,'expected_allow':expected,'actual_allow':actual})
    wildcard={'Statement':[{'Effect':'Allow','Action':'*','Resource':'*'}]}
    try:validate_policy(wildcard)
    except (ValueError,KeyError):results.append({'case':'wildcard policy rejected','passed':True})
    else:raise ValueError('wildcard policy accepted')
    print(json.dumps({'policy_checks':results,'scope':'local contract and limited policy model; no AWS requests'},indent=2))
    if args.image:
        image=json.loads(subprocess.check_output(['docker','image','inspect',args.image]))[0]
        if image['Config']['User']!='65532:65532':raise ValueError('wrong runtime UID')
        env=image['Config'].get('Env') or []
        if any(e.split('=',1)[0] in ['API_TOKEN','AWS_SECRET_ACCESS_KEY'] for e in env):raise ValueError('image secret ENV survived')
        program="""import os,json,errno,importlib.metadata
from app import app
c=app.test_client()
assert os.getuid()==65532 and os.getgid()==65532
assert c.get('/').status_code==200 and c.get('/').get_json()=={'app':'week13-demo','status':'ok'}
assert c.get('/health').get_json()=={'status':'healthy'}
assert 'API_TOKEN' not in os.environ and 'AWS_SECRET_ACCESS_KEY' not in os.environ
assert not os.path.exists('/app/Dockerfile.insecure')
assert not os.path.exists('/bin/sh') and not os.path.exists('/usr/bin/apt')
status=dict(x.split(':',1) for x in open('/proc/self/status') if ':' in x)
assert int(status['CapEff'].strip(),16)==0 and status['NoNewPrivs'].strip()=='1'
try:open('/tmp/week13-write-probe','w')
except OSError as e:assert e.errno==errno.EROFS
else:raise AssertionError('writable root filesystem')
print(json.dumps({'uid':os.getuid(),'gid':os.getgid(),'root':c.get('/').get_json(),'health':c.get('/health').get_json(),'image_secret_recovery':'both ENV keys absent; insecure Dockerfile absent','runtime':'read-only; zero effective capabilities; no-new-privileges; no network','Flask':importlib.metadata.version('flask'),'shell_absent':True},indent=2))
"""
        subprocess.run(['docker','run','--rm','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--memory','128m','--pids-limit','64','--network','none',args.image,'-c',program],check=True)
        print('PASS: image metadata, endpoint, secret-absence and runtime-boundary checks')
if __name__=='__main__':main()
