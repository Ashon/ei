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
    AWS_SECURITY_TOKEN,
    AWS_SESSION_EXPIRATION,
) = (
    os.getenv('EI_CREDENTIAL_RESOLVER', 'sts'),

    os.getenv('EI_ACCOUNT_IDS', '').split(','),
    os.getenv('EI_REGIONS', '').split(','),
    os.getenv('EI_STS_ASSUME_ROLE_ARN_PATTERN', ''),
    os.getenv('EI_STS_ASSUME_ROLE_SESSION_NAME', ''),
    os.getenv('AWS_REGION', ''),
    os.getenv('AWS_ACCESS_KEY_ID', ''),
    os.getenv('AWS_SECRET_ACCESS_KEY', ''),
    os.getenv('AWS_SECURITY_TOKEN', ''),
    os.getenv('AWS_SESSION_EXPIRATION', '')
)
