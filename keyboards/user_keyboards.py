from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_menu = KeyboardButton(text='Menu')
button_all_products = KeyboardButton(text='Hamma maxsulotlar')

button_case_user = ReplyKeyboardMarkup(
    resize_keyboard=True).add(button_menu).add(button_all_products)
