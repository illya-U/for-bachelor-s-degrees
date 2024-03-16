from typing import Union

from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bd_classes.initializeBD import SessionManager
from get_cred import get_cred
from telegram_bot.FinalStateMachine import LocationSender
from telegram_bot.routers.abstract_router import AbstractRouter


class CreatingLocationReportRouter(AbstractRouter):
    router: Router
    session: SessionManager
    bot: Bot

    def initialize_commands(self):
        self.router.message(F.location, LocationSender.creating_location_report)(self.handle_location)
        self.router.message(F.text, LocationSender.creating_location_report)(self.handle_description)
        # self.router.message(, LocationSender.creating_location_report)(self.handle_photo)

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
        pass


    # discussion to take this logic on middleware level(_answer_for_handle_point_on_the_map_addition and _get_not_fulfilled_requirements)

    async def _answer_for_handle_point_on_the_map_addition(self, message: types.Message, state: FSMContext, start_of_answer="") -> None:
        not_fulfilled_requirements = await self._get_not_fulfilled_requirements(state)

        if not_fulfilled_requirements:
            needed_requirements = ", ".join(not_fulfilled_requirements)
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




