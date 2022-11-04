import logging.config
from pathlib import Path

from aiogram import Bot, Dispatcher
from dependency_injector import containers, providers

from kv.mq.rpc import Producer
from kv.mq.scheme import RabbitConnectionSettings
from kv.service.transport import RPCService
from tg.bot import TelegramBot


project_root = Path(__file__).parent.parent


class ServiceContainer(containers.DeclarativeContainer):
    """Container for services."""

    config = providers.Configuration()
    settings = providers.Singleton(
        RabbitConnectionSettings,
        host=config.host,
        port=config.port,
        login=config.user,
        password=config.password,
        virtualhost=config.virtualhost,
    )
    producer = providers.Singleton(Producer, settings=settings)
    rpc = providers.Singleton(RPCService, producer=producer)


class TelegramContainer(containers.DeclarativeContainer):
    """BaseBot container."""

    config = providers.Configuration(yaml_files=[f"{project_root}/configurations/telegram.yaml"])
    bot = providers.Singleton(Bot, token=config.telegram.token)
    dispatcher = providers.Singleton(
        Dispatcher,
    )


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration(yaml_files=[f"{project_root}/configurations/core.yaml"])
    service = providers.Container(ServiceContainer, config=config.rabbit)
    aiogram = providers.Container(
        TelegramContainer,
    )
    bot = providers.Singleton(TelegramBot, service=service.rpc)
    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


__all__ = ("ApplicationContainer",)
