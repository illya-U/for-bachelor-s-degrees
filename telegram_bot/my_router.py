from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import UserProfilePhotos

from get_cred import get_cred


class MyRouter:
    def __init__(self, session, bot):
        self.router = Router()
        self.session = session
        self.bot = bot
        self.initialize_commands()

    def initialize_commands(self):
        self.router.message(Command(commands=['start']))(self.start_handler)
        self.router.message(Command(commands=['help']))(self.help_handler)

    def get_instance(self):
        return self.router

    async def help_handler(self, message: types.Message):
        await message.answer(
            f"Привіт, {message.from_user.full_name} це бот для контроля за станом сховищ міста Києва")

    async def start_handler(self, message: types.Message):
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        user_photos: UserProfilePhotos = await self.bot.get_user_profile_photos(user_id=user_id)

        if self.session.find_user_by_id(user_id):
            await message.answer("Надішліть мені свою геолокацію та фото, і я збережу цю інформацію у базі даних.")
            return

        user_photo_file_path = get_cred().get("user_photo_path")

        try:
            photo_id = user_photos.photos[0][0].file_id
            file_path = await self.bot.get_file(photo_id)

            user_photo_name = f"{user_id}_photo.jpg"

            await self.bot.download_file(file_path.file_path, user_photo_file_path + user_photo_name)
        except IndexError:
            print(f"User {user_id}, {user_name}, have no photo")
            user_photo_name = get_cred().get("default_photo_name")

        self.session.create_new_user(
            user_id=user_id,
            user_name=user_name,
            user_photo_path=user_photo_file_path + user_photo_name
        )

        await message.answer(
            "Привіт! Надішліть мені свою геолокацію та фото, і я збережу цю інформацію у базі даних.")


    # @dp.message(content_types=ContentType.LOCATION)
    # async def handle_location(message: types.Message):
    #     user_id = message.from_user.id
    #     location

    # @dp.errors_handler(exception = BotBlocked)
    # async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    #         print(f"Me blocked by user!\nMessage: {update}\nError: {exception}")
    #         return True
