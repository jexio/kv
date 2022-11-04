import io

from aiogram import Bot
from dependency_injector.wiring import Provide, inject


@inject
async def download(file_id: str, bot: Bot = Provide["aiogram.bot"]) -> io.BytesIO:
    """Download a file by ``file_id``.

    Args:
        file_id: Identifier for a file. :attr:`aiogram.types.Message.photo.file_id` e.g.
        bot: An instance of :class:`aiogram.Bot`.

    Returns:
        Buffered I/O.
    """
    file_io = io.BytesIO()
    await bot.download(file_id, destination=file_io)
    return file_io


__all__ = ("download",)
