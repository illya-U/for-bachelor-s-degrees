from typing import Union

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from get_cred import HostConfig
from ServiceLocator import ServiceLocator
from bd_classes.initializeBD import SessionManager
from FinalStateMachine import LocationSender
from routers.abstract_router import AbstractRouter

TR_TO_KEYS_MAP = {
    "location": "геолокація",
    "description": "опис що не так",
    "photo_path": "фотографію"
}


class CreatingLocationReportRouter(AbstractRouter):
    router: Router
    session: SessionManager
    cred: HostConfig

    def __init__(self):
        super().__init__()
        self.cred = ServiceLocator.get_service("credentials")

    def initialize_commands(self):
        self.router.message(F.location, LocationSender.creating_location_report)(self.handle_location)
        self.router.message(F.text, LocationSender.creating_location_report)(self.handle_description)
        self.router.message(F.photo, LocationSender.creating_location_report)(self.handle_photo)

    async def handle_location(self, message: types.Message, state: FSMContext):
        latitude = message.location.latitude
        longitude = message.location.longitude

        await state.update_data(location={
            "latitude": latitude,
            "longitude": longitude,
        })

        start_of_answer = f"Дякую, геолокація отримана! Широта: {latitude}, Довгота: {longitude}. "

        await self._answer_for_handle_point_on_the_map_addition(
            message,
            state,
            start_of_answer=start_of_answer
        )

    async def handle_description(self, message: types.Message, state: FSMContext):
        await state.update_data(description=message.text)

        start_of_answer = f"Дякую, інформацію отримана! "

        await self._answer_for_handle_point_on_the_map_addition(
            message,
            state,
            start_of_answer=start_of_answer
        )

    async def handle_photo(self, message: types.Message, state: FSMContext):
        start_of_answer = f"Дякую, фото отримано! "

        photo_path = await self._download_photo_location(
            bot=message.bot,
            photo_file_id=message.photo[-1].file_id
        )

        await state.update_data(photo_path=photo_path)

        await self._answer_for_handle_point_on_the_map_addition(
            message,
            state,
            start_of_answer=start_of_answer
        )

    # discussion to take this logic on middleware level(_answer_for_handle_point_on_the_map_addition and _get_not_fulfilled_requirements)
    async def _answer_for_handle_point_on_the_map_addition(self, message: types.Message, state: FSMContext, start_of_answer="") -> None:
        not_fulfilled_requirements = await self._get_not_fulfilled_requirements(state)

        if not_fulfilled_requirements:
            needed_requirements = ", ".join([TR_TO_KEYS_MAP.get(requirement, "невідома умова") for requirement in not_fulfilled_requirements])
            await message.reply(start_of_answer + f"Тобі залишилось надіслати тільки {needed_requirements}")
            return

        point_data = await state.get_data()

        self.session.add_point_on_the_map(
            user_id=message.from_user.id,
            location=point_data.get("location", {}),
            description=point_data.get("description", ""),
            photo_path=point_data.get("photo_path", "")
        )

        await state.clear()
        await message.reply(start_of_answer + f"Вітаю, данні записані до бази данних.", reply_markup=ReplyKeyboardRemove())

    async def _get_not_fulfilled_requirements(self, state: FSMContext) -> Union[list, bool]:
        point_data = await state.get_data()
        requirements = ["location", "description", "photo_path"]

        not_fulfilled_requirements = [requirement for requirement in requirements if requirement not in point_data.keys()]

        if not not_fulfilled_requirements:
            return False
        return not_fulfilled_requirements

    async def _download_photo_location(self, bot, photo_file_id) -> str:

        location_folder_photo_path = self.cred.LocationPhoto["location_folder_photo_path"]

        file_name = f"{photo_file_id}_photo.jpg"
        location_photo_path = location_folder_photo_path + file_name

        await bot.download(file=photo_file_id, destination=location_photo_path)
        return file_name






