from aiogram import Router, types, Bot, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import UserProfilePhotos

from bd_classes.initializeBD import SessionManager
from get_cred import get_cred
from telegram_bot.FinalStateMachine import LocationSender
from telegram_bot.inline_keyboard.send_location_button import text_send_location_button
from telegram_bot.routers.abstract_router import AbstractRouter


class CreatingLocationReportRouter(AbstractRouter):
    router: Router
    session: SessionManager
    bot: Bot

    def initialize_commands(self):
        self.router.message(F.location)(self.handle_location)

    async def handle_location(self, message: types.Message):
        # Ця функція буде викликатися, коли користувач надсилає свою геолокацію
        await message.answer(
            f"Геолокація отримана! Широта: {message.location.latitude}, Довгота: {message.location.longitude}")

    # @dp.errors_handler(exception = BotBlocked)
    # async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    #         print(f"Me blocked by user!\nMessage: {update}\nError: {exception}")
    #         return True
