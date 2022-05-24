from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_button = KeyboardButton("Cancel")
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

cancel_markup.add(cancel_button)