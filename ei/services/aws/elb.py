from typing import Any

import boto3
from mypy_boto3_elbv2 import ElasticLoadBalancingv2Client

from ei.core.service import BaseAwsService


class AwsElbLoadbalancerService(BaseAwsService):
    service_name = 'elbv2'

    @classmethod
    def _list(cls, client: ElasticLoadBalancingv2Client) -> Any:
        loadbalancers = [
            {**lb} for lb in client.describe_load_balancers()['LoadBalancers']
        ]

        loadbalancers = [{
            'ShortenId': str(lb['LoadBalancerArn']).split(':loadbalancer/')[1],
            **lb
        } for lb in loadbalancers]

        return loadbalancers

    @classmethod
    def _show(cls, client: ElasticLoadBalancingv2Client, id: str) -> Any:
        """Show Loadbalancer Object

        Fetch loadbalancer object and additional info.

        Additional info.

        - [green]Attributes[/green]: boto3.describe_load_balancer_attributes()
        - [green]Listener[/green]: boto3.describe_listeners()
        - [green]TargetGroups[/green]: boto3.describe_target_groups()
        - [green]Tags[/green]: boto3.describe_tags()
        """

        region_name = client._request_signer._region_name
        identity = boto3.client('sts').get_caller_identity()
        account_id = identity.get('Account')

        arn = (
            'arn:aws:elasticloadbalancing:'
            f'{region_name}:{account_id}:loadbalancer/{id}'
        )

        loadbalancer = client.describe_load_balancers(
            LoadBalancerArns=[arn])['LoadBalancers']
        attributes = client.describe_load_balancer_attributes(
            LoadBalancerArn=arn)
        listeners = client.describe_listeners(LoadBalancerArn=arn)
        target_groups = client.describe_target_groups(LoadBalancerArn=arn)
        tags = client.describe_tags(
            ResourceArns=[arn])['TagDescriptions'][0]['Tags']

        return [{
            'ShortenId': id,
            **loadbalancer[0],
            'Attributes': attributes.get('Attributes'),
            'Listeners': listeners.get('Listeners'),
            'TargetGroups': target_groups.get('TargetGroups'),
            'Tags': tags
        }]


class AwsElbListenerService(BaseAwsService):
    service_name = 'elbv2'

    @classmethod
    def _list(cls, client: ElasticLoadBalancingv2Client) -> Any:
        listeners = client.describe_listeners()['Listeners']
        return listeners

    @classmethod
    def _show(cls, client: ElasticLoadBalancingv2Client, id: str) -> Any:
        listener = client.describe_listeners(ListenerArns=[id])['Listeners']
        certificates = client.describe_listener_certificates(ListenerArn=id)
        rules = client.describe_rules(ListenerArn=id)

        tags = client.describe_tags(
            ResourceArns=[id])['TagDescriptions'][0]['Tags']

        return [{
            **listener[0],
            'Certificates': certificates.get('Certificates'),
            'Rules': rules.get('Rules'),
            'Tags': tags
        }]


class AwsElbTargetGroupService(BaseAwsService):
    service_name = 'elbv2'

    @classmethod
    def _list(cls, client: ElasticLoadBalancingv2Client) -> Any:
        target_groups = [
            {**tg} for tg in client.describe_target_groups()['TargetGroups']
        ]

        target_groups = [{
            'ShortenId': str(tg['TargetGroupArn']).split(':targetgroup/')[1],
            **tg
        } for tg in target_groups]

        return target_groups

    @classmethod
    def _show(cls, client: ElasticLoadBalancingv2Client, id: str) -> Any:
        region_name = client._request_signer._region_name
        identity = boto3.client('sts').get_caller_identity()
        account_id = identity.get('Account')

        arn = (
            'arn:aws:elasticloadbalancing:'
            f'{region_name}:{account_id}:targetgroup/{id}'
        )

        target_group = client.describe_target_groups(
            TargetGroupArns=[arn])['TargetGroups']

        attributes = client.describe_target_group_attributes(
            TargetGroupArn=arn)
        health = client.describe_target_health(TargetGroupArn=arn)
        tags = client.describe_tags(
            ResourceArns=[arn])['TagDescriptions'][0]['Tags']

        return [{
            'ShortenId': id,
            **target_group[0],
            'Certificates': attributes.get('Attributes'),
            'Rules': health.get('TargetHealthDescriptions'),
            'Tags': tags
        }]
