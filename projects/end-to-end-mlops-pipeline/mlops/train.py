"""Deterministic single-feature least-squares training and artifact export."""
import argparse,csv,hashlib,json
from pathlib import Path
from statistics import mean

def train(rows):
    points=[(float(r['x']),float(r['y'])) for r in rows]
    if len(points)<5:raise ValueError('at least five rows required')
    training=[p for i,p in enumerate(points) if i%5!=0]
    testing=[p for i,p in enumerate(points) if i%5==0]
    xm=mean([x for x,y in training]);ym=mean([y for x,y in training])
    variance=sum((x-xm)**2 for x,y in training)
    if variance==0:raise ValueError('feature has no variance')
    slope=sum((x-xm)*(y-ym) for x,y in training)/variance
    intercept=ym-slope*xm
    mae=mean(abs(y-(slope*x+intercept)) for x,y in testing)
    return {'schema_version':1,'model_type':'single_feature_ols','weights':{'x':slope,'intercept':intercept},'evaluation':{'mae':mae,'train_samples':len(training),'test_samples':len(testing)}}

def train_from_csv(source,destination):
    source=Path(source)
    with source.open(newline='',encoding='utf-8') as file: rows=list(csv.DictReader(file))
    artifact=train(rows)
    artifact['training_data_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    destination=Path(destination)
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(artifact,indent=2,sort_keys=True),encoding='utf-8')
    return artifact

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',default='datasets/training.csv')
    parser.add_argument('--output',default='artifacts/model.json')
    options=parser.parse_args()
    print(json.dumps(train_from_csv(options.data,options.output),indent=2))
if __name__=='__main__':main()
