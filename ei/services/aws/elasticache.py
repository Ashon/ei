from itertools import chain
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
        paginator = client.get_paginator(
            operation_name='describe_cache_clusters')
        clusters = chain(*[
            page['CacheClusters']
            for page in paginator.paginate()
        ])
        return clusters

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> Any:
        clusters = client.describe_cache_clusters(
            CacheClusterId=id)['CacheClusters']

        return clusters


class AwsElasticacheEventService(BaseAwsService):
    service_name = 'elasticache'

    @classmethod
    def _list(cls, client: ElastiCacheClient) -> Any:
        paginator = client.get_paginator(operation_name='describe_events')
        events = chain(*[
            page['Events']
            for page in paginator.paginate(Duration=60 * 24)
        ])
        return events

    # @classmethod
    # def _show(cls, client: ElastiCacheClient, id: str) -> Any:
    #     clusters = client.describe_cache_clusters(
    #         CacheClusterId=id)['CacheClusters']

    #     return clusters
