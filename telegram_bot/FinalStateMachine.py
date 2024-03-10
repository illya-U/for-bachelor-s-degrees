from aiogram.fsm.state import StatesGroup, State


class LocationSender(StatesGroup):
    registration_user = State()
    creating_location_report = State()
