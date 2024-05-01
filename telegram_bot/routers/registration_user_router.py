from aiogram import Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import UserProfilePhotos

from telegram_bot.get_cred import HostConfig
from telegram_bot.ServiceLocator import ServiceLocator
from telegram_bot.bd_classes.initializeBD import SessionManager
from telegram_bot.FinalStateMachine import LocationSender
from telegram_bot.inline_keyboard.send_location_button import get_send_location_button
from telegram_bot.routers.abstract_router import AbstractRouter


class RegistrationUserRouter(AbstractRouter):
    router: Router
    session: SessionManager
    bot: Bot
    cred: HostConfig

    def __init__(self):
        super().__init__()
        self.cred = ServiceLocator.get_service("credentials")

    def initialize_commands(self):
        self.router.message(Command(commands=['start']), StateFilter(None))(self.start_handler)

    async def start_handler(self, message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        user_photos: UserProfilePhotos = await message.bot.get_user_profile_photos(user_id=user_id)

        if self.session.find_user_by_id(user_id):
            await self.answer_for_start_handler(message=message, state=state, is_new_user=False)
            return

        user_photo_folder_path = self.cred.UserPhoto["user_folder_photo_path"]

        try:
            photo_id = user_photos.photos[0][0].file_id
            file_path = await message.bot.get_file(photo_id)

            user_photo_name = f"{user_id}_photo.jpg"

            await message.bot.download_file(file_path.file_path, user_photo_folder_path + user_photo_name)
        except IndexError:
            print(f"User {user_id}, {user_name}, have no photo")
            user_photo_name = self.cred.UserPhoto["default_photo_user_name"]

        self.session.create_new_user(
            user_id=user_id,
            user_name=user_name,
            user_photo_path=user_photo_folder_path + user_photo_name
        )

        await self.answer_for_start_handler(message=message, state=state, is_new_user=True)

    async def answer_for_start_handler(self, message: types.Message, state: FSMContext, is_new_user):
        new_user_message = "Привіт. Надішліть мені свою геолокацію та фото, і я збережу цю інформацію у базі даних."
        old_user_message = "Надішліть мені свою геолокацію та фото, і я збережу цю інформацію у базі даних."

        await message.answer(new_user_message if is_new_user else old_user_message, reply_markup=get_send_location_button())

        await state.set_state(LocationSender.creating_location_report)