import subprocess,json,pathlib,datetime,hashlib,sys
r=pathlib.Path(__file__).resolve().parents[1]/'evidence';p=r/'screenshots'/sys.argv[1]
a=datetime.datetime.now(datetime.timezone.utc);subprocess.run(['/usr/sbin/screencapture','-x',str(p)],check=True);b=datetime.datetime.now(datetime.timezone.utc)
record={'path':str(p),'capture_started_utc':a.isoformat(),'capture_finished_utc':b.isoformat(),'capture_finished_bangkok':b.astimezone(datetime.timezone(datetime.timedelta(hours=7))).isoformat(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'macOS screencapture -x; entire display; original unmodified PNG','visual_review':'pending'}
with (r/'task3-negative/captures.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
print(json.dumps(record))
