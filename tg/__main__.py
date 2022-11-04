import asyncio
import logging

from aiogram import Bot, Dispatcher
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from tg import utils
from tg.containers import ApplicationContainer
from tg.handlers import commands, photo, text


@inject
async def main(dp: Dispatcher = Provide["aiogram.dispatcher"], bot: Bot = Provide["aiogram.bot"]) -> None:
    """Entry point for the telegram bot listener.

    Args:
        dp: Root router.
        bot: An instance of :class:`aiogram.Bot`.
    """
    dp.include_router(commands.router)
    dp.include_router(text.router)
    dp.include_router(photo.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()
    container = ApplicationContainer()
    container.wire(modules=[__name__, text, photo, utils])
    logger = logging.getLogger(__name__)
    logger.debug("The Telegram bot has been launched.")
    asyncio.run(main())
