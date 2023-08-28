from typing import Any

from mypy_boto3_elbv2 import ElasticLoadBalancingv2Client

from ei.core.service import BaseAwsService


class BaseElasticLoadBalancerService(BaseAwsService):
    service_name = 'elbv2'


class AwsElbLoadbalancerService(BaseElasticLoadBalancerService):
    resource_name = 'LoadBalancers'

    @classmethod
    def _list(cls, client: ElasticLoadBalancingv2Client) -> Any:
        loadbalancers = client.describe_load_balancers()
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

        loadbalancer = client.describe_load_balancers(
            LoadBalancerArns=[id])['LoadBalancers']
        attributes = client.describe_load_balancer_attributes(
            LoadBalancerArn=id)
        listeners = client.describe_listeners(LoadBalancerArn=id)
        target_groups = client.describe_target_groups(LoadBalancerArn=id)
        tags = client.describe_tags(
            ResourceArns=[id])['TagDescriptions'][0]['Tags']

        return {
            'LoadBalancers': [{
                **loadbalancer[0],
                'Attributes': attributes.get('Attributes'),
                'Listeners': listeners.get('Listeners'),
                'TargetGroups': target_groups.get('TargetGroups'),
                'Tags': tags
            }]
        }


class AwsElbListenerService(BaseElasticLoadBalancerService):
    resource_name = 'Listeners'

    # @classmethod
    # def _list(cls, client: ElasticLoadBalancingv2Client) -> Any:
    #     listeners = client.describe_listeners()
    #     return listeners

    @classmethod
    def _show(cls, client: ElasticLoadBalancingv2Client, id: str) -> Any:
        listener = client.describe_listeners(ListenerArns=[id])['Listeners']
        certificates = client.describe_listener_certificates(ListenerArn=id)
        rules = client.describe_rules(ListenerArn=id)

        tags = client.describe_tags(
            ResourceArns=[id])['TagDescriptions'][0]['Tags']

        return {
            'Listeners': [{
                **listener[0],
                'Certificates': certificates.get('Certificates'),
                'Rules': rules.get('Rules'),
                'Tags': tags
            }]
        }


class AwsElbTargetGroupService(BaseElasticLoadBalancerService):
    resource_name = 'TargetGroups'

    @classmethod
    def _list(cls, client: ElasticLoadBalancingv2Client) -> Any:
        target_groups = client.describe_target_groups()
        return target_groups

    @classmethod
    def _show(cls, client: ElasticLoadBalancingv2Client, id: str) -> Any:
        target_group = client.describe_target_groups(
            TargetGroupArns=[id])['TargetGroups']

        attributes = client.describe_target_group_attributes(
            TargetGroupArn=id)
        health = client.describe_target_health(TargetGroupArn=id)
        tags = client.describe_tags(
            ResourceArns=[id])['TagDescriptions'][0]['Tags']

        return {
            'TargetGroups': [{
                **target_group[0],
                'Certificates': attributes.get('Attributes'),
                'Rules': health.get('TargetHealthDescriptions'),
                'Tags': tags
            }]
        }
