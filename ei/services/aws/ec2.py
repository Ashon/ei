from typing import Any
from typing import List
from typing import Union
from itertools import chain

from mypy_boto3_ec2 import EC2Client
from mypy_boto3_ec2.type_defs import TransitGatewayPeeringAttachmentTypeDef
from mypy_boto3_ec2.type_defs import TransitGatewayVpcAttachmentTypeDef
from mypy_boto3_ec2.type_defs import TransitGatewayAttachmentTypeDef
from mypy_boto3_ec2.type_defs import TransitGatewayTypeDef

from ei.core import defaults
from ei.core.exceptions import ResourceNotfoundError
from ei.core.service import BaseAwsService
from ei.core.utils import to_pascal_case


class BaseEC2Service(BaseAwsService):
    service_name = 'ec2'


class AwsEc2VpcService(BaseEC2Service):
    resource_name = 'Vpcs'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        return client.describe_vpcs()

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        return client.describe_vpcs(VpcIds=[id])


class AwsEc2SubnetService(BaseEC2Service):
    resource_name = 'Subnets'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        return client.describe_subnets()

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        return client.describe_subnets(SubnetIds=[id])


class AwsEc2SecurityGroupService(BaseEC2Service):
    resource_name = 'SecurityGroups'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        return client.describe_security_groups()

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        return client.describe_security_groups(GroupIds=[id])


class AwsEc2InstanceService(BaseEC2Service):
    resource_name = 'Instances'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        reservations = client.describe_instances()['Reservations']
        instances = [
            reservation['Instances']
            for reservation in reservations
        ]

        iterable = chain(*instances)

        return {'Instances': iterable}

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        reservations = client.describe_instances(
            InstanceIds=[id]
        )['Reservations']

        instance = [
            reservation['Instances']
            for reservation in reservations
        ]

        return {'Instances': instance}


class AwsEc2AmiService(BaseEC2Service):
    resource_name = 'Images'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        images = client.describe_images(
            Owners=defaults.EI_ACCOUNT_IDS)
        return images

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        image = client.describe_images(ImageIds=[id])

        return image


class AwsEc2RouteTableService(BaseEC2Service):
    resource_name = 'RouteTables'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        route_tables = client.describe_route_tables()
        return route_tables

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        route_table = client.describe_route_tables(
            RouteTableIds=[id])

        return route_table


class TransitGatewayNotFoundError(ResourceNotfoundError):
    pass


class AwsEc2TransitGatewayService(BaseEC2Service):
    resource_name = 'TransitGateways'

    TRANSIT_GATEWAY_ADDITIONAL_PROPERTIES = [
        # 'connect_peers',
        'connects',
        'multicast_domains',
        'policy_tables',
        'route_tables',
        'route_table_announcements',
    ]

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        transit_gateways = client.describe_transit_gateways()[
            'TransitGateways']
        populated_gateways = [
            cls._populate_transit_gateway(client, transit_gateway)
            for transit_gateway in transit_gateways
        ]
        return {'TransitGateways': populated_gateways}

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        transit_gateway = client.describe_transit_gateways(
            TransitGatewayIds=[id])['TransitGateways']

        found_transit_gateway = transit_gateway[0]
        if not found_transit_gateway:
            raise TransitGatewayNotFoundError(id)

        populated_transit_gateway = cls._populate_transit_gateway(
            client, found_transit_gateway)

        return {'TransitGateways': [populated_transit_gateway]}

    @classmethod
    def _populate_transit_gateway(
            cls, client: EC2Client,
            transit_gateway: TransitGatewayTypeDef) -> dict:
        """Fill Transit Gateway detail information

        See. TRANSIT_GATEWAY_ADDITIONAL_PROPERTIES
        """

        id = transit_gateway['TransitGatewayId']

        populated_transit_gateway: dict = {**transit_gateway}

        pop_keywords = [
            'TransitGatewayId',
            'TransitGatewayOwnerId',
            'Status'
        ]
        for property in cls.TRANSIT_GATEWAY_ADDITIONAL_PROPERTIES:
            fetcher = getattr(client, f'describe_transit_gateway_{property}')

            # try:
            result = fetcher(Filters=[{
                'Name': 'transit-gateway-id',
                'Values': [id]
            }])
            result = result[f'TransitGateway{to_pascal_case(property)}']
            for item in result:
                result_tags = item.pop('Tags')
                for keyword in pop_keywords:
                    if item.get(keyword):
                        item.pop(keyword)

                if result_tags:
                    name_tag = [
                        tag for tag in result_tags
                        if tag['Key'] == 'Name'
                    ]
                    if name_tag:
                        item['Name'] = name_tag[0]['Value']
                    else:
                        item['Name'] = ''

            populated_transit_gateway[to_pascal_case(property)] = result

        populated_transit_gateway['PeeringAttachments'] = (
            cls._list_transit_gateway_peering_attachments(client, id)
        )
        populated_transit_gateway['VpcAttachments'] = (
            cls._list_transit_gateway_vpc_attachments(client, id)
        )
        populated_transit_gateway['OtherAttachments'] = (
            cls._list_transit_gateway_other_attachments(client, id)
        )

        return populated_transit_gateway

    @classmethod
    def _refine_attachments(
            cls,
            attachments: Union[
                List[TransitGatewayPeeringAttachmentTypeDef],
                List[TransitGatewayVpcAttachmentTypeDef],
                List[TransitGatewayAttachmentTypeDef]
            ]) -> List[dict]:

        pop_keywords = [
            'TransitGatewayId',
            'TransitGatewayOwnerId',
            'Status'
        ]
        new_attachments = []
        for attachment in attachments:
            new_attachment = {**attachment}
            for keyword in pop_keywords:
                if new_attachment.get(keyword):
                    new_attachment.pop(keyword)

            result_tags: Any = new_attachment.get('Tags')
            if result_tags:
                new_attachment['Name'] = [
                    tag for tag in result_tags
                    if tag['Key'] == 'Name'
                ][0]['Value']
                new_attachment.pop('Tags')
            new_attachments.append(new_attachment)
        return new_attachments

    @classmethod
    def _list_transit_gateway_peering_attachments(
            cls, client: EC2Client, id: str) -> List[dict]:
        peering_attachments = (
            client.describe_transit_gateway_peering_attachments(
                Filters=[{
                    'Name': 'transit-gateway-id',
                    'Values': [id]
                }]
            )['TransitGatewayPeeringAttachments']
        )

        refined_attachments = cls._refine_attachments(peering_attachments)
        return refined_attachments

    @classmethod
    def _list_transit_gateway_vpc_attachments(
            cls, client: EC2Client, id: str) -> List[dict]:
        vpc_attachments = client.describe_transit_gateway_vpc_attachments(
            Filters=[{
                'Name': 'transit-gateway-id',
                'Values': [id]
            }])['TransitGatewayVpcAttachments']

        refined_attachments = cls._refine_attachments(vpc_attachments)
        return refined_attachments

    @classmethod
    def _list_transit_gateway_other_attachments(
            cls, client: EC2Client, id: str) -> List[dict]:
        attachments = client.describe_transit_gateway_attachments(
            Filters=[{
                'Name': 'transit-gateway-id',
                'Values': [id]
            }, {
                'Name': 'resource-type',
                'Values': [
                    'vpn',
                    'direct-connect-gateway',
                    'connect'
                ]
            }])['TransitGatewayAttachments']

        refined_attachments = cls._refine_attachments(attachments)
        return refined_attachments


class AwsEc2VpnGatewayService(BaseEC2Service):
    resource_name = 'VpnGateways'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        vpn_connections = client.describe_vpn_gateways()

        return vpn_connections

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        vpn_connections = client.describe_vpn_gateways(
            VpnGatewayIds=[id])

        return vpn_connections


class AwsEc2VpnConnectionService(BaseEC2Service):
    resource_name = 'VpnConnections'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        vpn_connections = client.describe_vpn_connections()

        return vpn_connections

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        vpn_connections = client.describe_vpn_connections(
            VpnConnectionIds=[id])

        return vpn_connections


class AwsEc2CustomerGatewayService(BaseEC2Service):
    resource_name = 'CustomerGateways'

    @classmethod
    def _list(cls, client: EC2Client) -> Any:
        customer_gateways = client.describe_customer_gateways()

        return customer_gateways

    @classmethod
    def _show(cls, client: EC2Client, id: str) -> Any:
        customer_gateways = client.describe_customer_gateways(
            CustomerGatewayIds=[id])

        return customer_gateways
