from aiogram import types


def get_send_location_button():
    text_send_location_button = "Відправити геолокацію"
    location_button = types.KeyboardButton(text=text_send_location_button, request_location=True)
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                location_button
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True)

    return keyboard