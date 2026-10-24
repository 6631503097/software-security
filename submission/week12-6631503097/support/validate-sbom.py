import json,pathlib,urllib.request,hashlib,collections,importlib.metadata
from referencing import Registry,Resource
from jsonschema import validators,FormatChecker
r=pathlib.Path(__file__).resolve().parents[1]/'evidence/task3';d=json.loads((r/'sbom.cdx.json').read_text());version=d['specVersion'];schemas=r/'schemas';schemas.mkdir(exist_ok=True)
retrieved=[]
def retrieve(uri):
 filename=uri.rsplit('/',1)[-1]
 if filename not in [f'bom-{version}.schema.json','spdx.schema.json','jsf-0.82.schema.json']:raise ValueError('Unexpected schema reference: '+uri)
 url='https://raw.githubusercontent.com/CycloneDX/specification/master/schema/'+filename
 data=(schemas/filename).read_bytes() if (schemas/filename).exists() else urllib.request.urlopen(url,timeout=30).read();(schemas/filename).write_bytes(data);retrieved.append({'url':url,'sha256':hashlib.sha256(data).hexdigest()});return Resource.from_contents(json.loads(data))
schema=retrieve(f'https://cyclonedx.org/schema/bom-{version}.schema.json').contents
cls=validators.validator_for(schema);cls.check_schema(schema);validator=cls(schema,registry=Registry(retrieve=retrieve),format_checker=FormatChecker());errors=sorted(validator.iter_errors(d),key=lambda e:str(list(e.path)))
flask=[c for c in d['components'] if c.get('name','').lower()=='flask'];(r/'flask-component.json').write_text(json.dumps(flask,indent=2)+'\n')
img=json.loads((r/'image-inspect.json').read_text())[0];props=d['metadata']['component']['properties'];sbom_id=next(p['value'] for p in props if p['name']=='aquasecurity:trivy:ImageID')
summary={'bomFormat':d['bomFormat'],'specVersion':version,'schema_validation':'PASS' if not errors else 'FAIL','jsonschema_version':importlib.metadata.version('jsonschema'),'validation_errors':[{'path':list(e.path),'message':e.message} for e in errors],'schemas':retrieved,'total_components':len(d['components']),'component_types':dict(collections.Counter(c['type'] for c in d['components'])),'purl_ecosystems':dict(collections.Counter(c.get('purl','').split('/')[0] for c in d['components'])),'dependency_nodes':len(d.get('dependencies',[])),'source_image_id':img['Id'],'sbom_image_id':sbom_id,'image_id_matches':img['Id']==sbom_id,'platform':img['Os']+'/'+img['Architecture'],'flask':flask,'sbom_sha256':hashlib.sha256((r/'sbom.cdx.json').read_bytes()).hexdigest()}
(r/'validation-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2));assert not errors;assert summary['image_id_matches'];assert len(flask)==1
