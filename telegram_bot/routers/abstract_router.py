from aiogram import Router
from abc import ABC, abstractmethod


class AbstractRouter(ABC):
    def __init__(self, session, bot):
        self.router = Router()
        self.session = session
        self.bot = bot
        self.initialize_commands()

    @abstractmethod
    def initialize_commands(self):
        pass

    def get_instance(self):
        return self.router

    # @self.router.message(content_types=ContentType.LOCATION)
    # async def handle_location(message: types.Message):
    #     user_id = message.from_user.id
    #     location

    # @dp.errors_handler(exception = BotBlocked)
    # async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    #         print(f"Me blocked by user!\nMessage: {update}\nError: {exception}")
    #         return True
