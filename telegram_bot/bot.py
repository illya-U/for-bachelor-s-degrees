from aiogram.types import BotCommand

from telegram_bot.routers.additional_router import AdditionalRouter
from telegram_bot.routers.creating_location_report_router import CreatingLocationReportRouter
from telegram_bot.routers.registration_user_router import RegistrationUserRouter
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
        session = ServiceLocator.get_service("session")
        bot = ServiceLocator.get_service("bot")
        dispatcher = ServiceLocator.get_service("dispatcher")

        self.registration_user_router = RegistrationUserRouter(
            session=session,
            bot=bot,
        )

        self.creating_location_report_router = CreatingLocationReportRouter(
            session=session,
            bot=bot,
        )

        self.additional_router = AdditionalRouter(
            session=session,
            bot=bot,
        )

        self.register_handlers(dispatcher)

    def register_handlers(self, dispatcher):
        dispatcher.include_router(self.registration_user_router.get_instance())
        dispatcher.include_router(self.creating_location_report_router.get_instance())
        dispatcher.include_router(self.additional_router.get_instance())