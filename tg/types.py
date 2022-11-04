import io
from enum import Enum
from typing import TypeVar


TInput = TypeVar("TInput", io.BytesIO, str)
TOutput = TypeVar("TOutput", io.BytesIO, str)


class TelegramContentType(Enum):
    """Supported types."""

    TEXT = "text"
    IMAGE = "photo"
    AUDIO = "audio"


__all__ = ("TelegramContentType", "TOutput", "TInput")
