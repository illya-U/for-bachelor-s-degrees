from aiogram.types import BotCommand

from telegram_bot.my_router import MyRouter
from ServiceLocator import ServiceLocator


async def set_commands():
    bot = ServiceLocator.get_service("bot")
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Помощь")
    ]
    await bot.set_my_commands(commands)


class BotManager:
    def __init__(self):
        self.router = MyRouter(
            session=ServiceLocator.get_service("session"),
            bot=ServiceLocator.get_service("bot"),
        )
        self.register_handlers(ServiceLocator.get_service("dispatcher"))

    def register_handlers(self, dispatcher):
        dispatcher.include_router(self.router.get_instance())
