from itertools import chain
from typing import Any

from mypy_boto3_elasticache.client import ElastiCacheClient

from ei.core.service import BaseAwsService


class BaseElasticacheService(BaseAwsService):
    service_name = 'elasticache'


class AwsElasticacheReplicationGroupService(BaseElasticacheService):
    @classmethod
    def _list(cls, client: ElastiCacheClient) -> Any:
        paginator = client.get_paginator(
            operation_name='describe_replication_groups')

        groups = chain(*[
            page['ReplicationGroups']
            for page in paginator.paginate()
        ])

        result = []
        for group in groups:
            tag = client.list_tags_for_resource(ResourceName=group['ARN'])
            result.append({**group, 'Tags': tag['TagList']})

        return result

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> Any:
        group = client.describe_replication_groups(
            ReplicationGroupId=id)['ReplicationGroups']

        tag = client.list_tags_for_resource(ResourceName=group[0]['ARN'])

        return [{**group[0], 'Tags': tag['TagList']}]


class AwsElasticacheCacheClusterService(BaseElasticacheService):
    @classmethod
    def _list(cls, client: ElastiCacheClient) -> Any:
        paginator = client.get_paginator(
            operation_name='describe_cache_clusters')

        clusters = chain(*[
            page['CacheClusters']
            for page in paginator.paginate()
        ])

        result = []
        for group in clusters:
            tag = client.list_tags_for_resource(ResourceName=group['ARN'])
            result.append({**group, 'Tags': tag['TagList']})

        return result

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> Any:
        clusters = client.describe_cache_clusters(
            CacheClusterId=id)['CacheClusters']

        tag = client.list_tags_for_resource(ResourceName=clusters[0]['ARN'])
        result = {**clusters[0], 'Tags': tag['TagList']}

        return [result]


class AwsElasticacheEventService(BaseElasticacheService):
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
