"""Disaster Recovery and Backup Automation.

Evaluate recovery point and time objectives.
Local, dependency-free educational prototype; not production infrastructure.
"""

def recovery_compliance(data_loss_minutes, restore_minutes, rpo_minutes, rto_minutes):
    return {'rpo_met':data_loss_minutes<=rpo_minutes, 'rto_met':restore_minutes<=rto_minutes}

if __name__ == '__main__':
    assert recovery_compliance(4,25,5,30)=={'rpo_met':True,'rto_met':True}
    print('Recovery objectives checked')
