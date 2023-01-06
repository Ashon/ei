from mypy_boto3_elasticache.client import ElastiCacheClient

from ei.aws._base import BaseAwsService


class AwsElasticacheReplicationGroupService(BaseAwsService):
    service_name = 'elasticache'

    @classmethod
    def _list(cls, client: ElastiCacheClient) -> list[dict]:
        groups = client.describe_replication_groups()['ReplicationGroups']
        return groups

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> list[dict]:
        group = client.describe_replication_groups(
            ReplicationGroupId=id)['ReplicationGroups']

        return group


class AwsElasticacheCacheClusterService(BaseAwsService):
    service_name = 'elasticache'

    @classmethod
    def _list(cls, client: ElastiCacheClient) -> list[dict]:
        clusters = client.describe_cache_clusters()['CacheClusters']
        return clusters

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> list[dict]:
        clusters = client.describe_cache_clusters(
            CacheClusterId=id)['CacheClusters']

        return clusters
