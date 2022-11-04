# flake8: noqa
import pytest
from dependency_injector import containers

from tg import utils
from tg.containers import ApplicationContainer
from tg.handlers import photo, text


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
def container() -> containers.DeclarativeContainer:
    container = ApplicationContainer()
    container.wire(modules=[text, photo, utils])
    return container
