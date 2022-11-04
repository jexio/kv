from unittest import mock

import pytest
from dependency_injector import containers

from tg.handlers import text


@pytest.mark.anyio
async def test_text_echo(container: containers.DeclarativeContainer) -> None:
    """Test the text handler.

    Args:
        container: A container for which the rpc service is being mocked.
    """
    service_mock = mock.AsyncMock()
    text_mock = "Hello, bot"
    service_mock.run.return_value = text_mock

    with container.service.rpc.override(service_mock):
        message_mock = mock.AsyncMock(text=text_mock)
        message_mock.content_type = "text"
        await text.get_text_messages(message=message_mock)
        message_mock.answer.assert_called_with(text_mock)
