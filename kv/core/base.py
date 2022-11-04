import abc
import logging
from typing import ClassVar, Generic, Optional, TypeVar

from tg.types import TInput, TOutput


T = TypeVar("T")
V = TypeVar("V")
K = TypeVar("K")
D = TypeVar("D")


class BaseService(Generic[T, V]):
    """This interface is designed to mark an object runnable."""

    def __init__(self) -> None:
        """Create a new instance of BaseService."""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abc.abstractmethod
    def run(self, command: str, *args, **kwargs) -> V:
        """Do some work here.

        Args:
            command: A name of command to run.
            *args: Command parameters.
            **kwargs: Command parameters.

        Raises:
            NotImplementedError: This is an abstract class method.
        """
        raise NotImplementedError("Method must be implemented in child class.")


class IMessageEncoder(Generic[T, K]):
    """This interface is designed to encode data."""

    @abc.abstractmethod
    def encode(self, message: T, data: TInput) -> K:
        """Encode your ``data`` to an appropriate format.

        Args:
            message: A message containing meta information.
            data: A data to encode.

        Raises:
            NotImplementedError: This is an abstract class method.
        """
        raise NotImplementedError("Method must be implemented in child class.")


class IMessageDecoder(Generic[K, T]):
    """This interface is designed to decode data."""

    @abc.abstractmethod
    def decode(self, message: T, data: K) -> TOutput:
        """Decode your ``data`` to an appropriate format.

        Args:
            message: A message containing meta information.
            data: A data to decode.

        Raises:
            NotImplementedError: This is an abstract class method.
        """
        raise NotImplementedError("Method must be implemented in child class.")


class IMessageHandler(IMessageEncoder[T, K], IMessageDecoder[K, T], metaclass=abc.ABCMeta):
    """This interface is designed to encode and decode data."""

    def __init__(self) -> None:
        self._handler: Optional[IMessageHandler] = None

    @property
    def handler(self) -> "IMessageHandler":
        """Get handler."""
        return self._handler

    @handler.setter
    def handler(self, handler: "IMessageHandler") -> None:
        """Set handler."""
        self._handler = handler


class BaseBot(abc.ABC, Generic[T]):
    """A class that handles user data."""

    _message_handler: ClassVar[IMessageHandler]
    _command: ClassVar[Optional[str]] = None

    def __init__(self, service: BaseService) -> None:
        """Create a new instance of BaseBot.

        Args:
            service: A service that processes the message in some way.
        """
        self._service = service

    async def handle(self, message: T, data: TInput) -> TOutput:
        """Receive a message, process it and send it back.

        Args:
            message: A message containing meta information.
            data: User data.

        Returns:
            Processed ``data`` in the appropriate format to send back to the user.
        """
        encoded_data = await self._message_handler.encode(message, data)
        processed_data = await self._service.run(self._command, data=encoded_data)
        result = await self._message_handler.decode(message, processed_data)
        return result


__all__ = ("BaseBot", "BaseService", "IMessageHandler")
