"""Inference from JSON artifacts, without unsafe object deserialization."""
import argparse,json
from pathlib import Path

def predict(model_path,x):
    model=json.loads(Path(model_path).read_text(encoding='utf-8'))
    if model['schema_version']!=1 or model['model_type']!='single_feature_ols':
        raise ValueError('unsupported artifact schema')
    return model['weights']['x']*float(x)+model['weights']['intercept']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',default='artifacts/model.json')
    parser.add_argument('--feature',type=float,required=True)
    options=parser.parse_args()
    print(json.dumps({'prediction':predict(options.model,options.feature)}))
if __name__=='__main__':main()
