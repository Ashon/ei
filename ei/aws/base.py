from typing import Any
from typing import List
from typing import Callable

from ei.aws import defaults
from ei.aws.session import client_session


class BaseAwsService(object):
    service_name: str

    @classmethod
    def _list(cls, client: object) -> List[dict]:
        """List diapatcher using client

        Should returns aws resource list

        Example =
            [
                {object A},
                {object B},
                {object C},
                ...
            ]
        """

        raise NotImplementedError('_list() dispatcher not implemented')

    @classmethod
    def _show(cls, client: object, id: str) -> dict:
        """Show diapatcher using aws client

        Should returns aws resource

        Example =
            {object A}
        """

        raise NotImplementedError('_show() dispatcher not implemented')

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
                {'Region': region, 'Account': account_id, **obj}
                for obj in result
            ]

        return result

    @classmethod
    def list(cls, region: str, account_id: str) -> List[dict]:
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
