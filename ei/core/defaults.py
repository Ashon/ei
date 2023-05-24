import os


CORES = os.cpu_count()

CONFIGS = (
    EI_CREDENTIAL_RESOLVER,

    EI_ACCOUNT_IDS,

    # use all regions
    # from botocore.args import LEGACY_GLOBAL_STS_REGIONS
    EI_REGIONS,

    # sts credential resolver config, if credential resolver is 'env', then
    # this configurations will be ignored.
    EI_STS_ASSUME_ROLE_ARN_PATTERN,
    EI_STS_ASSUME_ROLE_SESSION_NAME,

    AWS_REGION,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    # AWS_SECURITY_TOKEN,
    # AWS_SESSION_EXPIRATION,
) = (
    os.getenv('EI_CREDENTIAL_RESOLVER', 'sts'),

    os.getenv('EI_ACCOUNT_IDS', '').split(','),
    os.getenv('EI_REGIONS', '').split(','),
    os.getenv('EI_STS_ASSUME_ROLE_ARN_PATTERN', ''),
    os.getenv('EI_STS_ASSUME_ROLE_SESSION_NAME', ''),
    os.getenv('AWS_REGION', ''),
    os.getenv('AWS_ACCESS_KEY_ID', ''),
    os.getenv('AWS_SECRET_ACCESS_KEY', ''),
    # os.getenv('AWS_SECURITY_TOKEN', ''),
    # os.getenv('AWS_SESSION_EXPIRATION', '')
)


def print_config() -> str:
    return '\n'.join((
        f'EI_CREDENTIAL_RESOLVER={EI_CREDENTIAL_RESOLVER!r}',
        f'EI_ACCOUNT_IDS={EI_ACCOUNT_IDS}',
        f'EI_REGIONS={EI_REGIONS}',
        ('EI_STS_ASSUME_ROLE_ARN_PATTERN='
            f'{EI_STS_ASSUME_ROLE_ARN_PATTERN!r}'),
        ('EI_STS_ASSUME_ROLE_SESSION_NAME='
            f'{EI_STS_ASSUME_ROLE_SESSION_NAME!r}'),
        f'AWS_REGION={AWS_REGION!r}',
        f'AWS_ACCESS_KEY_ID={AWS_ACCESS_KEY_ID!r}',
        f'AWS_SECRET_ACCESS_KEY={AWS_SECRET_ACCESS_KEY!r}',
        # f'AWS_SECURITY_TOKEN={AWS_SECURITY_TOKEN!r}',
        # f'AWS_SESSION_EXPIRATION={AWS_SESSION_EXPIRATION!r}',
    ))
