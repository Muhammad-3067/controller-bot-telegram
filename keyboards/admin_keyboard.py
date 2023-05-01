from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

button_ypload = KeyboardButton(text='Yuklash')
button_cancel = KeyboardButton(text='Bekor qilish')
button_menu = KeyboardButton(text='Admin menu')
button_media_group = KeyboardButton(text='Rasmlar yuklash')
button_media_end = KeyboardButton(text="To'xtatish")

button_case_admin = ReplyKeyboardMarkup(
    resize_keyboard=True).row(button_ypload, button_menu).add(button_media_group)

button_cancel_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

button_media_end_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_media_end)
