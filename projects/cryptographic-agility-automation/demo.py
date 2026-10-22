"""Local proof-of-concept for cryptographic-agility-automation; not production-grade."""

def review_algorithms(inventory, deprecated=('RSA-1024','SHA-1','3DES')):
    return {'flagged':[name for name in inventory if name in deprecated], 'reviewed':len(inventory)}

if __name__=='__main__':
    assert review_algorithms(['SHA-1','SHA-256'])['flagged']==['SHA-1']
    print('Policy inventory passed')
