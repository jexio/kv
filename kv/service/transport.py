from typing import Any

from kv.core.base import BaseService
from kv.mq.rpc import Producer


class RPCService(BaseService[str, str]):
    """Service to call remote procedure."""

    def __init__(self, producer: Producer) -> None:
        """Create a new instance of RPCService.

        Args:
            producer: The object that runs your tasks on the server side.
        """
        super().__init__()
        self._producer = producer

    async def run(self, command: str, **kwargs) -> Any:
        """Execute a function by command name in a different address space.

        Args:
            command: A command name.
            **kwargs: Command parameters.

        Returns:
            Result of a remote procedure.
        """
        result = await self._producer.call(command, **kwargs)
        self.logger.info("Command %s has been successfully executed", command)
        return result
