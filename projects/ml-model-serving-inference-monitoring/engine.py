"""Production Machine Learning Model Serving and Inference Monitoring local evaluation engine."""
def evaluate(data):
    weights=[float(x) for x in data['weights']]
    inputs=[float(x) for x in data['features']]
    if len(weights)!=len(inputs) or not weights:raise ValueError('feature count mismatch')
    latency=float(data['latency_ms']);limit=float(data.get('latency_slo_ms',100))
    result=sum(x*w for x,w in zip(inputs,weights))+float(data.get('bias',0))
    return {'prediction':result,'latency_ms':latency,'latency_slo_met':latency<=limit,'feature_count':len(inputs)}

