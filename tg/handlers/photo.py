from aiogram import F, Router, types
from aiogram.types import BufferedInputFile
from dependency_injector.wiring import Provide, inject

from kv.core.base import BaseBot
from tg.utils.media import download


router = Router()


# flake8: noqa: RST306
@router.message(F.photo)
@inject
async def get_photo_messages(message: types.Message, bot_: BaseBot = Provide["bot"]) -> None:
    """Handle text data here.

    Args:
        message: User message.
        bot_: An instance of :class:`kv.core.base.BaseBot`.
    """
    file_io = await download(message.photo[-1].file_id)
    result = await bot_.handle(message, file_io)
    await message.answer_photo(photo=BufferedInputFile(file=result.read(), filename=""))


__all__ = ("router",)
