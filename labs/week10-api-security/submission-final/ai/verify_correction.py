from pathlib import Path
import datetime,zoneinfo,getpass,importlib.util,json,hashlib
from werkzeug.security import check_password_hash
b=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('draft_corrected_api',b/'corrected_api.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.app.config['TESTING']=True
client=m.app.test_client()
print(f'{getpass.getuser()} | 6631503097 | {datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Bangkok")).isoformat()}')
print('Command: .venv/bin/python verify_correction.py')
print('MODE: Flask in-process test_client. No network requests; not deployed to 8080/8081.')
count=0
def send(label,method,path,**kwargs):
    global count
    count+=1
    print(f'\nCASE {count}: {label}\n{method.upper()} {path}\ninput: {json.dumps(kwargs)}')
    r=getattr(client,method)(path,**kwargs)
    print('HTTP '+r.status)
    print(str(r.headers),end='')
    print(r.get_data(as_text=True))
    return r
payload=dict(username='mallory',password='x',is_admin=True,balance=1000000)
r=send('exact worksheet exploit','post','/api/users',json=payload)
assert r.status_code==201
user=r.get_json();assert user==dict(id=4,username='mallory',balance=0,is_admin=False)
assert 'password' not in user and 'password_hash' not in user
stored=m.USERS[4];assert 'password' not in stored and check_password_hash(stored['password_hash'],'x')
print('PASS: escalation blocked; public fields exact; stored hash verifies and no plaintext is stored.')
r=send('client id and hash cannot bind','post','/api/users',json=dict(username='second',password='x',id=999,password_hash='attacker',is_admin=True,balance=77))
assert r.status_code==201 and r.get_json()['id']==5 and not r.get_json()['is_admin']
assert m.USERS[5]['password_hash']!='attacker'
print('PASS: generated id and hash override all injected fields.')
invalid=[None,[],{},dict(username='a'),dict(username=1,password='x'),dict(username='a',password=True),dict(username='  ',password='x'),dict(username='a'*65,password='x'),dict(username='a',password=''),dict(username='a',password='x'*129)]
for value in invalid:
    before=(len(m.USERS),m._next_id)
    r=send('invalid JSON shape or field','post','/api/users',data=json.dumps(value),content_type='application/json')
    assert r.status_code==400 and before==(len(m.USERS),m._next_id)
r=send('malformed JSON','post','/api/users',data='{',content_type='application/json');assert r.status_code==400
print('PASS: all invalid creation requests rejected without allocating users or ids.')
for username,password,expected in [('mallory','wrong',401),('mallory','x',200),('alice','alice123',200)]:
    r=send('hashed login compatibility','post','/api/login',json=dict(username=username,password=password));assert r.status_code==expected
    assert 'password' not in r.get_json() and 'password_hash' not in r.get_json()
print('PASS: new and seeded logins work; wrong password rejected.')
for n,h in json.loads((b/'source-hashes.json').read_text()).items():assert hashlib.sha256((b.parent.parent/n).read_bytes()).hexdigest()==h
print(f'\nALL CHECKS PASSED: {count} in-process requests. Original API source hashes unchanged.')
print('Limitations: toy X-User-Id identity remains; in-memory users/limiter/ID allocation are not concurrency-safe or distributed; username uniqueness, production password policy, login malformed-input handling and deployment hardening remain out of scope.')
