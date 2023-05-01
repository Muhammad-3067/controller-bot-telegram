from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

count_users = KeyboardButton(text="Foydalanuvchilar")

creator_count_users = ReplyKeyboardMarkup(resize_keyboard=True).add(count_users)