import asyncio
import gzip
from typing import Any, ParamSpec

from aio_pika import connect_robust
from aio_pika.patterns import JsonRPC

from kv.constructor import RPC_FUNCTIONS
from kv.mq.scheme import RabbitConnectionSettings


P = ParamSpec("P")


class JsonGZipRPC(JsonRPC):
    CONTENT_TYPE = "application/octet-stream"

    def serialize(self, data: Any) -> bytes:
        """Serialize data using gzip.

        Args:
            data: data to serialize.

        Returns:
            Serialized data.
        """
        return gzip.compress(super().serialize(data))

    def deserialize(self, data: Any) -> bytes:
        """Deserialize data using gzip.

        Args:
            data: data to deserialize.

        Returns:
            Deserialized data.
        """
        return super().deserialize(gzip.decompress(data))


class Consumer:
    """Helper which implements Remote Procedure Call pattern."""

    def __init__(self, settings: RabbitConnectionSettings) -> None:
        """Create a new instance of Consumer.

        Args:
            settings: Connection settings.
        """
        self._settings = settings

    async def start(self) -> None:
        """Start a server."""
        connection = await connect_robust(**self._settings.dict())

        # Creating channel
        channel = await connection.channel()
        rpc = await JsonGZipRPC.create(channel)
        for name, function_ in RPC_FUNCTIONS:
            await rpc.register(name, function_, auto_delete=True)

        try:
            await asyncio.Future()
        finally:
            await connection.close()


class Producer:
    """Helper which implements Remote Procedure Call pattern."""

    def __init__(self, settings: RabbitConnectionSettings) -> None:
        """Create a new instance of Producer.

        Args:
            settings: Connection settings.
        """
        self._settings = settings

    async def call(self, function_name: str, **kwargs: P.kwargs) -> Any:
        """Call remote method and awaiting result.

        Args:
            function_name: Name of method.
            **kwargs: Command parameters.

        Returns:
            Result of a remote procedure.
        """
        connection = await connect_robust(**self._settings.dict())

        async with connection:
            # Creating channel
            channel = await connection.channel()
            rpc = await JsonGZipRPC.create(channel)

            # Creates task by proxy object
            result = await rpc.call(function_name, kwargs=kwargs)

        return result


__all__ = ("Producer", "Consumer")
