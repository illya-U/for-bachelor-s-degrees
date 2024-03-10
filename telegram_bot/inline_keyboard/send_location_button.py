from aiogram import types

text_send_location_button = "Відправити геолокацію"


def get_send_location_button():
    location_button = types.KeyboardButton(text=text_send_location_button, request_location=True)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                location_button
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True)

    return keyboard