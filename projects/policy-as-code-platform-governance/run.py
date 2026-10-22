import json,sys
from engine import evaluate
if __name__=='__main__':
    with open(sys.argv[1] if len(sys.argv)>1 else 'examples/scenario.json') as f: scenario=json.load(f)
    print(json.dumps(evaluate(scenario),indent=2,sort_keys=True))
