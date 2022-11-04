"""Functions representing remote methods."""
from typing import Any

from kv.constructor import RPC_FUNCTIONS


@RPC_FUNCTIONS.register_class
def nothing(data: Any) -> Any:
    """Do nothing.

    Args:
        data: Any data.

    Returns:
        The same data.
    """
    return data
