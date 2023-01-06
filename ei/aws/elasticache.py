from typing import Any

from mypy_boto3_elasticache.client import ElastiCacheClient

from ei.core.service import BaseAwsService


class AwsElasticacheReplicationGroupService(BaseAwsService):
    service_name = 'elasticache'

    @classmethod
    def _list(cls, client: ElastiCacheClient) -> Any:
        groups = client.describe_replication_groups()['ReplicationGroups']
        return groups

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> Any:
        group = client.describe_replication_groups(
            ReplicationGroupId=id)['ReplicationGroups']

        return group


class AwsElasticacheCacheClusterService(BaseAwsService):
    service_name = 'elasticache'

    @classmethod
    def _list(cls, client: ElastiCacheClient) -> Any:
        clusters = client.describe_cache_clusters()['CacheClusters']
        return clusters

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> Any:
        clusters = client.describe_cache_clusters(
            CacheClusterId=id)['CacheClusters']

        return clusters
