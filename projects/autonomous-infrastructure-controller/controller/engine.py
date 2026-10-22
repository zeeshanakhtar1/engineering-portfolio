"""Policy-bounded autoscaling recommendation with audit."""
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import json
from pathlib import Path

@dataclass(frozen=True)
class Policy:
    minimum:int=1
    maximum:int=5
    scale_out_at:float=.80
    scale_in_at:float=.25
    cooldown_seconds:int=60
    max_step:int=1

@dataclass(frozen=True)
class Decision:
    replicas_before:int
    replicas_after:int
    utilization:float
    action:str
    reason:str
    execute:bool=False

def decide(replicas:int,utilization:float,seconds_since_last_change:float,policy:Policy=Policy())->Decision:
    if not 0<=utilization<=1 or policy.minimum<1 or policy.maximum<policy.minimum or not policy.minimum<=replicas<=policy.maximum or policy.max_step<1:
        raise ValueError('invalid controller inputs')
    if not 0<=policy.scale_in_at<policy.scale_out_at<=1:
        raise ValueError('invalid thresholds')
    if seconds_since_last_change<policy.cooldown_seconds:
        return Decision(replicas,replicas,utilization,'hold','cooldown')
    if utilization>policy.scale_out_at and replicas<policy.maximum:
        return Decision(replicas,min(policy.maximum,replicas+policy.max_step),utilization,'scale_out','high_utilization')
    if utilization<policy.scale_in_at and replicas>policy.minimum:
        return Decision(replicas,max(policy.minimum,replicas-policy.max_step),utilization,'scale_in','low_utilization')
    return Decision(replicas,replicas,utilization,'hold','healthy_or_at_boundary')

class AuditLog:
    def __init__(self,path):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)
    def append(self,decision):
        event={'timestamp':datetime.now(timezone.utc).isoformat(),**asdict(decision)}
        with self.path.open('a',encoding='utf-8') as handle:
            handle.write(json.dumps(event)+'\n')
        return event
