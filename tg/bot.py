# flake8: noqa
import base64
import io

from aiogram import types

from kv.core.base import BaseBot, IMessageHandler
from tg.types import TelegramContentType, TInput, TOutput


class TelegramTextHandler(IMessageHandler[types.Message, str]):
    async def decode(self, message: types.Message, data: str) -> TOutput:
        if message.content_type == TelegramContentType.TEXT.value:
            return data
        else:
            return await self._handler.decode(message, data)

    async def encode(self, message: types.Message, data: str) -> str:
        if message.content_type == TelegramContentType.TEXT.value:
            return data
        else:
            return await self._handler.encode(message, data)


class TelegramImageHandler(IMessageHandler[types.Message, str]):
    async def decode(self, message: types.Message, data: str) -> TOutput:
        if message.content_type == TelegramContentType.IMAGE.value:
            data = base64.b64decode(data)
            file_ = io.BytesIO(data)
            return file_
        else:
            return await self._handler.decode(message, data)

    async def encode(self, message: types.Message, data: io.BytesIO) -> str:
        if message.content_type == TelegramContentType.IMAGE.value:
            image = base64.b64encode(data.read()).decode()
            return image
        else:
            return await self._handler.encode(message, data)


class TelegramMessageHandler(IMessageHandler[types.Message, TInput]):
    def __init__(self) -> None:
        super().__init__()
        self._handler = TelegramTextHandler()
        self._handler.handler = TelegramImageHandler()

    async def encode(self, message: types.Message, data: TInput) -> TInput:
        return await self._handler.encode(message, data)

    async def decode(self, message: types.Message, data: TInput) -> TOutput:
        return await self._handler.decode(message, data)


class TelegramBot(BaseBot[types.Message]):
    _message_handler = TelegramMessageHandler()
    _command = "nothing"
