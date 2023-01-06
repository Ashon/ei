import sys

import typer

from ei.cli import ec2
from ei.cli import vpc
from ei.aws import defaults


APPS = [
    ec2.Ec2CliApp,
    vpc.VpcCliApp
]


def main():
    try:
        defaults.preflight()

    except defaults.PreflightError:
        print('Check environment variables')
        print()
        print(f'{defaults.EI_ACCOUNT_IDS=}')
        print(f'{defaults.EI_REGIONS=}')
        print(f'{defaults.EI_ASSUME_ROLE_ARN_PATTERN=}')
        print(f'{defaults.EI_ASSUME_ROLE_SESSION_NAME=}')
        print(f'{defaults.AWS_REGION=}')
        print(f'{defaults.AWS_ACCESS_KEY_ID=}')
        print(f'{defaults.AWS_SECRET_ACCESS_KEY=}')
        print(f'{defaults.AWS_SECURITY_TOKEN=}')
        print(f'{defaults.AWS_SESSION_EXPIRATION=}')

        sys.exit(1)

    cli = typer.Typer()

    for app in APPS:
        obj = app()
        cli.add_typer(obj.typer())

    return cli


cli = main()
