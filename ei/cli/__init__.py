
from ei.cli import ami
from ei.cli import ec2
from ei.cli import elasticache
from ei.cli import vpc


APPS = [
    ec2.Ec2CliApp,
    ami.AmiCliApp,
    vpc.VpcCliApp,
    elasticache.ReplicationGroupCliApp,
    elasticache.CacheClusterCliApp,
]

__all__ = ['APPS']
