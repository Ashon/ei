# from typing import Type

from ei.core.cli import BaseCliApp
from ei.core.cli import CliGroup
from ei.core.fields import Field
from ei.core.fields import IDField
from ei.core.fields import BooleanField
from ei.core.fields import TagField
from ei.core.fields import DictField
from ei.services.aws.rds import AwsRdsInstanceService


group = CliGroup(name='rds', description='AWS RDS')


@group.app
class Ec2RdsInstanceCli(BaseCliApp):
    name: str = 'instance'
    description: str = 'EC2 RDS'

    service_cls = AwsRdsInstanceService

    short_fields = (
        IDField('DBInstanceIdentifier'),
        Field('DBInstanceClass'),
        Field('Engine'),
        Field('EngineVersion'),
        Field('DBInstanceStatus'),
    )

    long_fields = (
        BooleanField('PubliclyAccessible'),
        BooleanField('StorageEncrypted'),
    )

    detail_fields = (
        Field('AvailabilityZone'),
        Field('AutomaticRestartTime'),
        Field('MasterUsername'),
        Field('DBName'),
        Field('AllocatedStorage'),
        Field('InstanceCreateTime'),
        Field('PreferredBackupWindow'),
        Field('BackupRetentionPeriod'),
        Field('PreferredMaintenanceWindow'),
        Field('LatestRestorableTime'),
        BooleanField('MultiAZ'),
        BooleanField('AutoMinorVersionUpgrade'),
        Field('ReadReplicaSourceDBInstanceIdentifier'),
        Field('ReplicaMode'),
        Field('LicenseModel'),
        Field('Iops'),
        Field('CharacterSetName'),
        Field('NcharCharacterSetName'),
        Field('SecondaryAvailabilityZone'),
        Field('StorageType'),
        Field('TdeCredentialArn'),
        Field('DbInstancePort'),
        Field('DBClusterIdentifier'),

        Field('KmsKeyId'),
        Field('DbiResourceId'),
        Field('CACertificateIdentifier'),
        BooleanField('CopyTagsToSnapshot'),
        Field('MonitoringInterval'),
        Field('EnhancedMonitoringResourceArn'),
        Field('MonitoringRoleArn'),
        Field('PromotionTier'),
        Field('DBInstanceArn'),
        Field('Timezone'),
        BooleanField('IAMDatabaseAuthenticationEnabled'),
        BooleanField('PerformanceInsightsEnabled'),
        Field('PerformanceInsightsKMSKeyId'),
        Field('PerformanceInsightsRetentionPeriod'),
        BooleanField('DeletionProtection'),
        Field('MaxAllocatedStorage'),
        BooleanField('CustomerOwnedIpEnabled'),
        Field('AwsBackupRecoveryPointArn'),
        Field('ActivityStreamStatus'),
        Field('ActivityStreamKmsKeyId'),
        Field('ActivityStreamKinesisStreamName'),
        Field('ActivityStreamMode'),
        Field('ActivityStreamEngineNativeAuditFieldsIncluded'),
        Field('AutomationMode'),
        Field('ResumeFullAutomationModeTime'),
        Field('CustomIamInstanceProfile'),
        Field('BackupTarget'),
        Field('NetworkType'),
        Field('ActivityStreamPolicyStatus'),
        Field('StorageThroughput'),
        Field('DBSystemId'),
        DictField('Endpoint'),
        DictField('DBSecurityGroups'),
        DictField('VpcSecurityGroups'),
        DictField('DBParameterGroups'),
        DictField('DBSubnetGroup'),
        DictField('PendingModifiedValues'),
        DictField('OptionGroupMemberships'),
        DictField('DomainMemberships'),
        DictField('AssociatedRoles'),
        Field('ReadReplicaDBInstanceIdentifiers'),
        Field('ReadReplicaDBClusterIdentifiers'),
        Field('StatusInfos'),
        Field('EnabledCloudwatchLogsExports'),
        Field('ProcessorFeatures'),
        Field('ListenerEndpoint'),
        Field('DBInstanceAutomatedBackupsReplications'),
        Field('MasterUserSecret'),
        Field('CertificateDetails'),
        TagField('TagList'),
    )
