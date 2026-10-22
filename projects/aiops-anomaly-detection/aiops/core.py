"""Robust univariate anomaly detection with a minimum history gate."""
from dataclasses import dataclass
from statistics import median
from typing import Iterable

@dataclass(frozen=True)
class Detection:
    metric: str
    value: float
    baseline: float
    robust_z: float
    anomalous: bool
    reason: str

def detect(metric: str, history: Iterable[float], value: float, *, threshold: float=3.5, min_history: int=5) -> Detection:
    values=[float(item) for item in history]
    if min_history<3 or threshold<=0:
        raise ValueError('invalid detector configuration')
    if len(values)<min_history:
        return Detection(metric,float(value),0.0,0.0,False,'insufficient_history')
    baseline=median(values)
    mad=median([abs(item-baseline) for item in values])
    score=(1e12 if value!=baseline else 0.0) if mad==0 else abs(0.6745*(value-baseline)/mad)
    return Detection(metric,float(value),baseline,score,score>threshold,'anomaly' if score>threshold else 'normal')
