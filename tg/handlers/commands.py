from aiogram import Router, types
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message) -> None:
    """This handler will be called when user sends `/start` command.

    Args:
        message: User message.
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


__all__ = ("router",)
