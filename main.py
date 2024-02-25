import logging
import asyncio

from bd_classes.initializeBD import session_initialization

from aiogram import Bot, Dispatcher
from sys import exit

from telegram_bot.bot import BotManager, set_commands
from get_cred import get_cred
from ServiceLocator import ServiceLocator


def on_startup():
    print("connect to database")
    session_initialization()
    BotManager()


async def main():
    print("Bot start")

    CRED = get_cred()
    BOT_TOKEN = CRED.get("BOT_TOKEN")
    if not BOT_TOKEN:
        exit("Error: no token provided")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)

    ServiceLocator.register_service("bot", bot)
    ServiceLocator.register_service("dispatcher", dp)

    await set_commands()

    on_startup()

    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())