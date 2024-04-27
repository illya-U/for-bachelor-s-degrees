import logging
import asyncio

from bd_classes.initializeBD import session_initialization

from aiogram import Bot, Dispatcher
from sys import exit

from telegram_bot.bot import BotManager, set_commands
from get_cred import HostConfig
from telegram_bot.ServiceLocator import ServiceLocator


def on_startup():
    print("connect to database")
    session_initialization()
    BotManager()


async def main():
    print("Bot start")

    cred = HostConfig()
    bot_token = cred.TelegramBot["BOT_TOKEN"]
    if not bot_token:
        exit("Error: no token provided")
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)

    ServiceLocator.register_service("dispatcher", dp)
    ServiceLocator.register_service("credentials", cred)

    await set_commands(bot)

    on_startup()

    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())