from typing import Type
from ei.core.cli import BaseCliApp
from ei.core.service import BaseAwsService
from ei.core.fields import Field
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.aws.elasticache import AwsElasticacheReplicationGroupService
from ei.aws.elasticache import AwsElasticacheCacheClusterService


class ReplicationGroupCliApp(BaseCliApp):
    name: str = 'replicationgroup'
    description: str = 'Elasticache replication group'

    service_cls: Type[BaseAwsService] = AwsElasticacheReplicationGroupService

    short_fields = (
        Field('Region'),
        Field('Account'),
        Field('ReplicationGroupId'),
        Field('Status'),
        Field('AutomaticFailover'),
        Field('MultiAZ'),
        Field('ClusterEnabled'),
        Field('CacheNodeType'),
    )

    long_fields = (
        Field('AuthTokenEnabled'),
        Field('TransitEncryptionEnabled'),
        Field('AtRestEncryptionEnabled'),
        Field('AutoMinorVersionUpgrade'),
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


class CacheClusterCliApp(BaseCliApp):
    name: str = 'cachecluster'
    description: str = 'Elasticache cache cluster'

    service_cls: Type[AwsElasticacheCacheClusterService] = (
        AwsElasticacheCacheClusterService)

    short_fields = (
        Field('Region'),
        Field('Account'),
        Field('CacheClusterId'),
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
        Field('AuthTokenEnabled'),
        Field('TransitEncryptionEnabled'),
        Field('AtRestEncryptionEnabled'),
        Field('AutoMinorVersionUpgrade'),
        Field('ReplicationGroupLogDeliveryEnabled'),
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
