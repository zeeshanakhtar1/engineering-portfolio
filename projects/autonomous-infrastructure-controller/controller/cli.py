"""Non-mutating infrastructure controller CLI."""
import argparse,json
from dataclasses import asdict
from .engine import AuditLog,Policy,decide

def main():
    parser=argparse.ArgumentParser(description='Evaluate policy-bounded scaling decisions')
    parser.add_argument('--replicas',type=int,required=True)
    parser.add_argument('--utilization',type=float,required=True)
    parser.add_argument('--last-change-seconds',type=float,default=3600)
    parser.add_argument('--minimum',type=int,default=1)
    parser.add_argument('--maximum',type=int,default=5)
    parser.add_argument('--audit-file',default='/tmp/controller/audit.jsonl')
    opts=parser.parse_args()
    result=decide(opts.replicas,opts.utilization,opts.last_change_seconds,Policy(minimum=opts.minimum,maximum=opts.maximum))
    AuditLog(opts.audit_file).append(result)
    print(json.dumps(asdict(result),sort_keys=True))

if __name__=='__main__':main()
