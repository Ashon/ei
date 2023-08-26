from typing import Type
from ei.core.cli import BaseCliApp
from ei.core.cli import CliGroup
from ei.core.service import BaseAwsService
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import BooleanField
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.services.aws.elasticache import AwsElasticacheReplicationGroupService
from ei.services.aws.elasticache import AwsElasticacheCacheClusterService
from ei.services.aws.elasticache import AwsElasticacheEventService


group = CliGroup(name='elasticache', description='AWS Elasticache')


@group.app
class ElasticacheReplicationGroupCli(BaseCliApp):
    name: str = 'replicationgroup'
    description: str = 'Elasticache replication group'

    service_cls: Type[BaseAwsService] = AwsElasticacheReplicationGroupService

    stats_fields = [
        'Region', 'Account', 'ClusterEnabled', 'CacheNodeType', 'Status']

    short_fields = [
        IDField('ReplicationGroupId'),
        Field('Status'),
        Field('AutomaticFailover'),
        Field('MultiAZ'),
        BooleanField('ClusterEnabled'),
        Field('CacheNodeType'),
    ]

    long_fields = [
        BooleanField('AuthTokenEnabled'),
        BooleanField('TransitEncryptionEnabled'),
        BooleanField('AtRestEncryptionEnabled'),
        BooleanField('AutoMinorVersionUpgrade'),
        Field('ReplicationGroupCreateTime'),
        Field('SnapshotWindow'),
        Field('SnapshotRetentionLimit'),
        DictField('ConfigurationEndpoint'),
        Field('PendingModifiedValues'),
        Field('LogDeliveryConfigurations'),
        TagField('Tags')
    ]

    detail_fields = [
        Field('NetworkType'),
        Field('IpDiscovery'),
        Field('ARN'),
        Field('GlobalReplicationGroupInfo'),
        Field('Description'),
        DictField('NodeGroups'),
        Field('MemberClusters'),
    ]


@group.app
class ElasticacheCacheClusterCli(BaseCliApp):
    name: str = 'cachecluster'
    description: str = 'Elasticache cache cluster'

    service_cls: Type[AwsElasticacheCacheClusterService] = (
        AwsElasticacheCacheClusterService)

    stats_fields = ['Region', 'Account', 'Engine']

    short_fields = [
        IDField('CacheClusterId'),
        Field('CacheNodeType'),
        Field('Engine'),
        Field('EngineVersion'),
        Field('CacheClusterStatus'),
        Field('NumCacheNodes'),
    ]

    long_fields = [
        Field('CacheSubnetGroupName'),
        Field('ReplicationGroupId'),
        Field('PreferredAvailabilityZone'),
        Field('PreferredMaintenanceWindow'),
        Field('CacheClusterCreateTime'),
        TagField('Tags')
    ]

    detail_fields = [
        Field('ARN'),
        BooleanField('AuthTokenEnabled'),
        BooleanField('TransitEncryptionEnabled'),
        BooleanField('AtRestEncryptionEnabled'),
        BooleanField('AutoMinorVersionUpgrade'),
        BooleanField('ReplicationGroupLogDeliveryEnabled'),
        Field('NetworkType'),
        Field('IpDiscovery'),
        Field('SnapshotRetentionLimit'),
        Field('SnapshotWindow'),
        DictField('CacheParameterGroup'),
        Field('LogDeliveryConfigurations'),
        DictField('SecurityGroups'),
        DictField('PendingModifiedValues'),
        Field('CacheSecurityGroups'),
        Field('ClientDownloadLandingPage'),
    ]


@group.app
class ElasticacheEventCli(BaseCliApp):
    name: str = 'event'
    description: str = 'Elasticache event'

    service_cls = AwsElasticacheEventService

    short_fields = [
        Field('SourceIdentifier'),
        Field('SourceType'),
        Field('Message'),
        Field('Date'),
    ]

    long_fields = []
    detail_fields = []
