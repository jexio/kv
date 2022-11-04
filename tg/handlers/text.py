from aiogram import F, Router, types
from dependency_injector.wiring import Provide, inject

from kv.core.base import BaseBot


router = Router()


# flake8: noqa: RST306
@router.message(F.text)
@inject
async def get_text_messages(message: types.Message, bot_: BaseBot = Provide["bot"]) -> None:
    """Handle image data here.

    Args:
        message: User message.
        bot_: An instance of :class:`kv.core.base.BaseBot`.
    """
    result = await bot_.handle(message, message.text)
    await message.answer(result)


__all__ = ("router",)
