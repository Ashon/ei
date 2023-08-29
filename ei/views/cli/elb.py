
from ei.core.cli import BaseCliApp
from ei.core.cli import CliGroup
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import TagField
from ei.core.fields import BooleanField
from ei.core.fields import DictField
from ei.core.fields import extract
from ei.services.aws.elb import AwsElbLoadbalancerService
from ei.services.aws.elb import AwsElbListenerService
from ei.services.aws.elb import AwsElbTargetGroupService


group = CliGroup(name='elb', description='AWS ElasticLoadbalancer')


@group.app
class ElbLoadbalancerCli(BaseCliApp):
    name: str = 'loadbalancer'
    description: str = 'ElasticLoadbalancer Loadbalander'
    service_cls = AwsElbLoadbalancerService
    stats_fields = ['Region', 'Account', 'Type']
    short_fields = [
        IDField('LoadBalancerArn'),
        Field('LoadBalancerName'),
        Field('State', serializer=extract('Code')),
        Field('Type'),
    ]
    long_fields = [
        Field('IpAddressType'),
        Field('Scheme'),
        Field('CreatedTime'),
        Field('CanonicalHostedZoneId'),
    ]
    detail_fields = [
        Field('VpcId'),
        Field('DNSName'),
        DictField('Attributes'),
        DictField('AvailabilityZones'),
        DictField('Listeners'),
        DictField('TargetGroups'),
        TagField('Tags')
    ]


@group.app
class ElbListenerCli(BaseCliApp):
    name: str = 'listener'
    description: str = 'ElasticLoadbalancer Listener'
    service_cls = AwsElbListenerService
    short_fields = [
        IDField('ListenerArn'),
        Field('LoadBalancerArn'),
        Field('Port'),
        Field('Protocol'),
    ]
    long_fields = []
    detail_fields = [
        DictField('DefaultActions'),
        DictField('Certificates'),
        DictField('Rules'),
        TagField('Tags')
    ]


@group.app
class ElbTargetGroupCli(BaseCliApp):
    name: str = 'targetgroup'
    description: str = 'ElasticLoadbalancer TargetGroup'
    service_cls = AwsElbTargetGroupService
    short_fields = [
        IDField('TargetGroupArn'),
        Field('TargetGroupName'),
        Field('Protocol'),
        Field('Port'),
        BooleanField('HealthCheckEnabled'),
        Field('TargetType'),
    ]
    long_fields = [
        Field('HealthCheckProtocol'),
        Field('HealthCheckPort'),
        Field('HealthCheckIntervalSeconds'),
        Field('HealthCheckTimeoutSeconds'),
        Field('HealthyThresholdCount'),
        Field('UnhealthyThresholdCount'),
        Field('HealthCheckPath'),
    ]
    detail_fields = [
        Field('VpcId'),
        Field('ProtocolVersion'),
        Field('IpAddressType'),
        DictField('Matcher'),
        Field('LoadBalancerArns'),
        DictField('DefaultActions'),
        DictField('Certificates'),
        DictField('Rules'),
        TagField('Tags')
    ]
