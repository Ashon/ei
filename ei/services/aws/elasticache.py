from typing import List

from itertools import chain
from typing import Any

from mypy_boto3_elasticache.client import ElastiCacheClient
from mypy_boto3_elasticache.type_defs import TagTypeDef

from ei.core.service import BaseAwsService


class BaseElasticacheService(BaseAwsService):
    service_name = 'elasticache'

    @classmethod
    def _tags(cls, client: ElastiCacheClient,
              resource_arn: str) -> List[TagTypeDef]:
        tags = client.list_tags_for_resource(ResourceName=resource_arn)

        return tags['TagList']


class AwsElasticacheReplicationGroupService(BaseElasticacheService):
    resource_name = 'ReplicationGroups'

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
            tags = cls._tags(client, group['ARN'])
            result.append({**group, 'Tags': tags})

        return {'ReplicationGroups': result}

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> Any:
        group = client.describe_replication_groups(
            ReplicationGroupId=id)['ReplicationGroups']

        tags = cls._tags(client, group[0]['ARN'])

        return {'ReplicationGroups': [{**group[0], 'Tags': tags}]}


class AwsElasticacheCacheClusterService(BaseElasticacheService):
    resource_name = 'CacheClusters'

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
            tags = cls._tags(client, group['ARN'])
            result.append({**group, 'Tags': tags})

        return {'CacheClusters': result}

    @classmethod
    def _show(cls, client: ElastiCacheClient, id: str) -> Any:
        clusters = client.describe_cache_clusters(
            CacheClusterId=id)['CacheClusters']

        tags = cls._tags(client, clusters[0]['ARN'])

        return {'CacheClusters': [{**clusters[0], 'Tags': tags}]}


class AwsElasticacheEventService(BaseElasticacheService):
    resource_name = 'Events'

    @classmethod
    def _list(cls, client: ElastiCacheClient) -> Any:
        paginator = client.get_paginator(operation_name='describe_events')
        events = chain(*[
            page['Events']
            for page in paginator.paginate(Duration=60 * 24)
        ])
        return {'Events': events}

    # @classmethod
    # def _show(cls, client: ElastiCacheClient, id: str) -> Any:
    #     clusters = client.describe_cache_clusters(
    #         CacheClusterId=id)['CacheClusters']

    #     return clusters
