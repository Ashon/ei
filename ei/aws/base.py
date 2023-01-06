from typing import Any
from typing import Callable

from ei.aws import defaults
from ei.aws.session import client_session


class BaseAwsService(object):
    service_name: str

    @classmethod
    def _list(cls, client: object) -> list[dict]:
        raise NotImplementedError()

    @classmethod
    def _show(cls, client: object, id: str) -> dict:
        raise NotImplementedError()

    @classmethod
    def _defaulting_args(cls, region: str, account_id: str) -> tuple:
        if not region:
            region = defaults.AWS_REGION

        if not account_id:
            account_id = defaults.EI_ACCOUNT_IDS[0]

        return region, account_id

    @classmethod
    def _dispatch(cls, fn: Callable, region: str, account_id: str,
                  *args, **kwargs) -> Any:
        """Dispatching resources by command
        """

        result = None

        with client_session(
                account_id=account_id, region=region,
                service_name=cls.service_name) as client:

            result = fn(client, *args, **kwargs)
            result = [
                {'Region': region, **obj}
                for obj in result
            ]

        return result

    @classmethod
    def list(cls, region: str, account_id: str) -> list[dict]:
        region, account_id = cls._defaulting_args(region, account_id)
        result = cls._dispatch(
            cls._list, region=region, account_id=account_id)

        return result

    @classmethod
    def show(cls, id: str, region: str, account_id: str) -> dict:
        region, account_id = cls._defaulting_args(region, account_id)
        result = cls._dispatch(
            cls._show, region=region, account_id=account_id, id=id)[0]

        return result
