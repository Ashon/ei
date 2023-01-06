from ei.aws.fixtures import vpc


def list():
    return vpc.DUMMY_VPC


def show(id: int):
    return vpc.DUMMY_VPC[0]
