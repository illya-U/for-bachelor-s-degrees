from aiogram.types import BotCommand

from routers.additional_router import AdditionalRouter
from routers.creating_location_report_router import CreatingLocationReportRouter
from routers.registration_user_router import RegistrationUserRouter
from ServiceLocator import ServiceLocator


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/help", description="Помощь")
    ]
    await bot.set_my_commands(commands)


class BotManager:
    def __init__(self):
        self.registration_user_router = RegistrationUserRouter()

        self.creating_location_report_router = CreatingLocationReportRouter()

        self.additional_router = AdditionalRouter()

        self.register_handlers(ServiceLocator.get_service("dispatcher"))

    def register_handlers(self, dispatcher):
        dispatcher.include_router(self.registration_user_router.get_instance())
        dispatcher.include_router(self.creating_location_report_router.get_instance())
        dispatcher.include_router(self.additional_router.get_instance())