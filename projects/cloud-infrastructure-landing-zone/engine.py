"""Production-Ready Cloud Infrastructure and Landing Zone: local-first domain-specific engine."""
from ipaddress import ip_network
def evaluate(data):
    networks=[ip_network(value,strict=False) for value in data['subnets']]
    overlap=[(str(a),str(b)) for i,a in enumerate(networks) for b in networks[i+1:] if a.overlaps(b)]
    forbidden=[str(item) for item in networks if item.is_global]
    return {'cidr_overlap':overlap,'publicly_routable_subnets':forbidden,'segmentation_valid':not overlap and not forbidden,'provisioned':False}

