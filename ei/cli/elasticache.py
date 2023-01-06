from ei.cli._base import BaseCliApp
from ei.aws.elasticache import AwsElasticacheReplicationGroupService
from ei.aws.elasticache import AwsElasticacheCacheClusterService
from ei.core.field_serializers import serialize_tags
from ei.core.field_serializers import serialize_dict_list


class ReplicationGroupCliApp(BaseCliApp):
    name: str = 'replicationgroup'
    description: str = 'Elasticache replication group'

    service_cls = AwsElasticacheReplicationGroupService

    short_fields = (
        ('Region', str),
        ('Account', str),
        ('ReplicationGroupId', str),
        ('Status', str),
        ('AutomaticFailover', str),
        ('MultiAZ', str),
        ('ClusterEnabled', str),
        ('CacheNodeType', str),
    )

    long_fields = (
        ('AuthTokenEnabled', str),
        ('TransitEncryptionEnabled', str),
        ('AtRestEncryptionEnabled', str),
        ('AutoMinorVersionUpgrade', str),
        ('ReplicationGroupCreateTime', str),
        ('SnapshotWindow', str),
        ('SnapshotRetentionLimit', str),
        ('ConfigurationEndpoint', str),
        ('PendingModifiedValues', str),
        ('LogDeliveryConfigurations', str),
        ('Tags', serialize_tags)
    )

    detail_fields = (
        ('NetworkType', str),
        ('IpDiscovery', str),
        ('ARN', str),
        ('GlobalReplicationGroupInfo', str),
        ('Description', str),
        ('NodeGroups', serialize_dict_list),
        ('MemberClusters', str),
    )


class CacheClusterCliApp(BaseCliApp):
    name: str = 'cachecluster'
    description: str = 'Elasticache cache cluster'

    service_cls = AwsElasticacheCacheClusterService

    short_fields = (
        ('Region', str),
        ('Account', str),
        ('CacheClusterId', str),
        ('CacheNodeType', str),
        ('Engine', str),
        ('EngineVersion', str),
        ('CacheClusterStatus', str),
        ('NumCacheNodes', str),
    )

    long_fields = (
        ('CacheSubnetGroupName', str),
        ('ReplicationGroupId', str),
        ('PreferredAvailabilityZone', str),
        ('PreferredMaintenanceWindow', str),
        ('CacheClusterCreateTime', str),
        ('Tags', serialize_tags)
    )

    detail_fields = (
        ('ARN', str),
        ('AuthTokenEnabled', str),
        ('TransitEncryptionEnabled', str),
        ('AtRestEncryptionEnabled', str),
        ('AutoMinorVersionUpgrade', str),
        ('ReplicationGroupLogDeliveryEnabled', str),
        ('NetworkType', str),
        ('IpDiscovery', str),
        ('SnapshotRetentionLimit', str),
        ('SnapshotWindow', str),
        ('CacheParameterGroup', str),
        ('LogDeliveryConfigurations', str),
        ('SecurityGroups', str),
        ('PendingModifiedValues', str),
        ('CacheSecurityGroups', str),
        ('ClientDownloadLandingPage', str),
    )
