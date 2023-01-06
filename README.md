# A`[ei]`WS CLI

aws cli for humans

## Installation

``` sh
pip install git+https://github.com/ashon-lee/ei@0.0.1
```

## Configuration

``` sh
# set environment variables

# comma seperated account ids
EI_ACCOUNT_IDS='000000000000,111111111111'

# comma seperated region list
EI_REGIONS='ap-northeast-1,ap-northeast-2,ca-central-1,eu-west-2'

# sts assume role pattern for cross account
EI_ASSUME_ROLE_ARN_PATTERN='arn:aws:iam::{account_id}:role/my-awesome-role'
EI_ASSUME_ROLE_SESSION_NAME='AssumeRoleEi'

# use aws-vault for resolve aws environment vars
AWS_REGION=None
AWS_ACCESS_KEY_ID=None
AWS_SECRET_ACCESS_KEY=None
AWS_SECURITY_TOKEN=None
AWS_SESSION_EXPIRATION=None
```

## Run

``` sh
$ ei --help

# ec2 commands
$ ei ec2 list
$ ei ec2 show {instance-id}

# vpc commands
$ ei vpc list
$ ei vpc show {vpc-id}
```

Using aws-vault for cross account, region resource retrieving.

```

# list vpcs across all regions, and all accounts ($EI_REGIONS, $EI_ACCOUNT_IDS)
$ aws-vault exec {aws-vault-profile} -- ei vpc list --all-regions --all-accounts

# same as ec2
$ aws-vault exec {aws-vault-profile} -- ei ec2 list --all-regions --all-accounts

...
```
