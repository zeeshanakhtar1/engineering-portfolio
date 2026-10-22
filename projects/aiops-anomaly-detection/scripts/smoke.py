import json
from urllib.request import Request,urlopen
BASE='http://127.0.0.1:8091'
with urlopen(BASE+'/healthz',timeout=5) as response:
    assert json.load(response)['status']=='ok'
for value in [10,11,10,11,10,11,100]:
    req=Request(BASE+'/v1/ingest',json.dumps({'metric':'cpu_test','value':value}).encode(),{'Content-Type':'application/json'})
    with urlopen(req,timeout=5) as response:
        result=json.load(response)
assert result['anomalous'] is True,result
print('AIOps end-to-end ingest and anomaly smoke test passed')
