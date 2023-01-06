# A`[ei]`WS CLI

aws cli for humans

## Installation

Install via [pypi](https://pypi.org/project/ei-cli/)

``` sh
pip install ei-cli
```

Install via github

``` sh
pip install git+https://github.com/ashon/ei@0.0.7
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

## Development

This project controlled by [Hatch](https://github.com/pypa/hatch).

``` sh
$ pip install hatch

# install package as editable mode
$ pip install -e .

# testing commands
$ hatch run lint
$ hatch run test
$ hatch run typecheck
```
