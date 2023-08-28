import os
from typing import Any
from typing import List
from typing import Type
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Query
from pydantic_settings import BaseSettings

import ei
from ei.core import defaults
from ei.core.concurrency import bulk_action
from ei.core.service import BaseAwsService


ROOT_DIR = os.path.dirname(ei.__file__)


class Config(BaseSettings):
    log_level: str = 'INFO'


def pascal_to_kebab(pascal_str: str) -> str:
    kebab_str = ''
    for i in range(len(pascal_str)):
        if pascal_str[i].isupper():
            if i != 0 and (pascal_str[i-1].islower() or (
                    i + 1 < len(pascal_str) and pascal_str[i + 1].islower())):
                kebab_str += '-'
        kebab_str += pascal_str[i].lower()
    return kebab_str


def create_service_router(service: BaseAwsService) -> APIRouter:
    router = APIRouter(
        prefix=f'/{service.service_name}', tags=[service.service_name])
    resource_name = pascal_to_kebab(service.resource_name)
    singular = resource_name[:-1]

    if service._list.__code__ is not BaseAwsService._list.__code__:
        description = f'List {service.service_name} {service.resource_name}'

        @router.get(f'/{resource_name}', description=description,
                    summary=description)
        def list_resources(
                region: Optional[str] = None,
                account_id: Optional[str] = None) -> list:
            regions: list = [region]
            if not region:
                regions = defaults.EI_REGIONS

            account_ids: list = [account_id]
            if not account_id:
                account_ids = defaults.EI_ACCOUNT_IDS
            results = [*bulk_action(service.list, regions, account_ids)]

            return results

    if service._show.__code__ is not BaseAwsService._show.__code__:
        description = f'Show {service.service_name} {service.resource_name}'

        @router.get('/' + resource_name + '/{' + singular + '-id}',
                    description=description, summary=description)
        def show_resource(
                region: str,
                account_id: str,
                resource_id: str = Query(alias=f'{singular}-id')) -> Any:
            result = service.show(resource_id, region, account_id)

            return result

    return router


def create_server(service_classes: List[Type[BaseAwsService]]) -> FastAPI:
    app = FastAPI(
        title='EI',
        description='AWS Retrieve API'
    )

    for service_cls in service_classes:
        service = service_cls()
        app.include_router(
            prefix='/api',
            router=create_service_router(service)
        )

    return app


def start_server(service_classes: List[Type[BaseAwsService]],
                 listen_addr: str) -> None:
    """Start ei http server
    """

    config = Config()

    listen_host, listen_port = listen_addr.split(':')
    asgi = create_server(service_classes)

    uvicorn.run(
        asgi,
        log_level=config.log_level.lower(),
        loop='uvloop',
        host=listen_host,
        port=int(listen_port),
        reload_dirs=[ROOT_DIR],
    )
