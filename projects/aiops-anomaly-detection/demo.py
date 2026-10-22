"""AIOps Anomaly Detection.

Detect metric outliers using a transparent baseline.
Local, dependency-free educational prototype; not production infrastructure.
"""

def anomalies(baseline, observations, tolerance):
    if not baseline or tolerance<0: raise ValueError('invalid baseline')
    avg=sum(baseline)/len(baseline)
    return [i for i,x in enumerate(observations) if abs(x-avg)>tolerance]

if __name__ == '__main__':
    assert anomalies([10,10,10],[10,30,9],5)==[1]
    print('Anomaly detection passed')
