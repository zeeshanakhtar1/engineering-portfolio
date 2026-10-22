"""ML Model Serving and Inference Monitoring.

Validate inference requests and latency service objectives.
Local, dependency-free educational prototype; not production infrastructure.
"""

def inference_response(features, weights, latency_ms, slo_ms=100):
    if len(features)!=len(weights): raise ValueError('feature mismatch')
    return {'prediction':sum(x*w for x,w in zip(features,weights)), 'slo_met':latency_ms<=slo_ms}

if __name__ == '__main__':
    assert inference_response([1,2],[3,4],10)['prediction']==11
    print('Inference validation passed')
