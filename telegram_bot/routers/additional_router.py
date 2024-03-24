from aiogram import types, Router, Bot
from aiogram.filters import Command, StateFilter

from bd_classes.initializeBD import SessionManager
from telegram_bot.routers.abstract_router import AbstractRouter


class AdditionalRouter(AbstractRouter):
    router: Router
    session: SessionManager

    def initialize_commands(self):
        self.router.message(Command(commands=['help']))(self.help_handler)

    async def help_handler(self, message: types.Message):
        await message.answer(
            f"Привіт, {message.from_user.full_name} це бот для контроля за станом сховищ міста Києва")

    # @dp.errors_handler(exception = BotBlocked)
    # async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    #         print(f"Me blocked by user!\nMessage: {update}\nError: {exception}")
    #         return True
