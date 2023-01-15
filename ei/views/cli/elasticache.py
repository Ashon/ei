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


group = CliGroup(name='elasticache', description='AWS Elasticache')


@group.app
class ReplicationGroupCliApp(BaseCliApp):
    name: str = 'replicationgroup'
    description: str = 'Elasticache replication group'

    service_cls: Type[BaseAwsService] = AwsElasticacheReplicationGroupService

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('ReplicationGroupId'),
        Field('Status'),
        Field('AutomaticFailover'),
        Field('MultiAZ'),
        BooleanField('ClusterEnabled'),
        Field('CacheNodeType'),
    )

    long_fields = (
        BooleanField('AuthTokenEnabled'),
        BooleanField('TransitEncryptionEnabled'),
        BooleanField('AtRestEncryptionEnabled'),
        BooleanField('AutoMinorVersionUpgrade'),
        Field('ReplicationGroupCreateTime'),
        Field('SnapshotWindow'),
        Field('SnapshotRetentionLimit'),
        Field('ConfigurationEndpoint'),
        Field('PendingModifiedValues'),
        Field('LogDeliveryConfigurations'),
        TagField('Tags')
    )

    detail_fields = (
        Field('NetworkType'),
        Field('IpDiscovery'),
        Field('ARN'),
        Field('GlobalReplicationGroupInfo'),
        Field('Description'),
        DictField('NodeGroups'),
        Field('MemberClusters'),
    )


@group.app
class CacheClusterCliApp(BaseCliApp):
    name: str = 'cachecluster'
    description: str = 'Elasticache cache cluster'

    service_cls: Type[AwsElasticacheCacheClusterService] = (
        AwsElasticacheCacheClusterService)

    short_fields = (
        Field('Region'),
        Field('Account'),
        IDField('CacheClusterId'),
        Field('CacheNodeType'),
        Field('Engine'),
        Field('EngineVersion'),
        Field('CacheClusterStatus'),
        Field('NumCacheNodes'),
    )

    long_fields = (
        Field('CacheSubnetGroupName'),
        Field('ReplicationGroupId'),
        Field('PreferredAvailabilityZone'),
        Field('PreferredMaintenanceWindow'),
        Field('CacheClusterCreateTime'),
        TagField('Tags')
    )

    detail_fields = (
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
        Field('CacheParameterGroup'),
        Field('LogDeliveryConfigurations'),
        Field('SecurityGroups'),
        Field('PendingModifiedValues'),
        Field('CacheSecurityGroups'),
        Field('ClientDownloadLandingPage'),
    )
