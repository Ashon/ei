from ei.cli._base import BaseCliApp
from ei.aws.elasticache import AwsElasticacheReplicationGroupService
from ei.aws.elasticache import AwsElasticacheCacheClusterService
from ei.core.field_serializers import to_string
from ei.core.field_serializers import serialize_tags
from ei.core.field_serializers import serialize_dict_list


class ReplicationGroupCliApp(BaseCliApp):
    name: str = 'replicationgroup'
    description: str = 'Elasticache replication group'

    service_cls = AwsElasticacheReplicationGroupService

    short_fields = (
        ('Region', to_string),
        ('Account', to_string),
        ('ReplicationGroupId', to_string),
        ('Status', to_string),
        ('AutomaticFailover', to_string),
        ('MultiAZ', to_string),
        ('ClusterEnabled', to_string),
        ('CacheNodeType', to_string),
    )

    long_fields = (
        ('AuthTokenEnabled', to_string),
        ('TransitEncryptionEnabled', to_string),
        ('AtRestEncryptionEnabled', to_string),
        ('AutoMinorVersionUpgrade', to_string),
        ('ReplicationGroupCreateTime', to_string),
        ('SnapshotWindow', to_string),
        ('SnapshotRetentionLimit', to_string),
        ('ConfigurationEndpoint', to_string),
        ('PendingModifiedValues', to_string),
        ('LogDeliveryConfigurations', to_string),
        ('Tags', serialize_tags)
    )

    detail_fields = (
        ('NetworkType', to_string),
        ('IpDiscovery', to_string),
        ('ARN', to_string),
        ('GlobalReplicationGroupInfo', to_string),
        ('Description', to_string),
        ('NodeGroups', serialize_dict_list),
        ('MemberClusters', to_string),
    )


class CacheClusterCliApp(BaseCliApp):
    name: str = 'cachecluster'
    description: str = 'Elasticache cache cluster'

    service_cls = AwsElasticacheCacheClusterService

    short_fields = (
        ('Region', to_string),
        ('Account', to_string),
        ('CacheClusterId', to_string),
        ('CacheNodeType', to_string),
        ('Engine', to_string),
        ('EngineVersion', to_string),
        ('CacheClusterStatus', to_string),
        ('NumCacheNodes', to_string),
    )

    long_fields = (
        ('CacheSubnetGroupName', to_string),
        ('ReplicationGroupId', to_string),
        ('PreferredAvailabilityZone', to_string),
        ('PreferredMaintenanceWindow', to_string),
        ('CacheClusterCreateTime', to_string),
        ('Tags', serialize_tags)
    )

    detail_fields = (
        ('ARN', to_string),
        ('AuthTokenEnabled', to_string),
        ('TransitEncryptionEnabled', to_string),
        ('AtRestEncryptionEnabled', to_string),
        ('AutoMinorVersionUpgrade', to_string),
        ('ReplicationGroupLogDeliveryEnabled', to_string),
        ('NetworkType', to_string),
        ('IpDiscovery', to_string),
        ('SnapshotRetentionLimit', to_string),
        ('SnapshotWindow', to_string),
        ('CacheParameterGroup', to_string),
        ('LogDeliveryConfigurations', to_string),
        ('SecurityGroups', to_string),
        ('PendingModifiedValues', to_string),
        ('CacheSecurityGroups', to_string),
        ('ClientDownloadLandingPage', to_string),
    )
