from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from bot_file import bot
from database import sqlite_db
from keyboards import user_keyboards
from messages import search
HELP_TEXT = """
/help --> Yordam menusi
Menu --> Oxirgi qoshilgan 5 maxsulotni ko'rsatadi
Hamma maxsulotlar --> Barcha maxsulotlarni ko'rsatadi

Bu bot guruhda jonatilayotgan ssilkalarni ochiradi,
adminlardan boshqalar qoshmoqchi bo'lgan botlarni qoshishga yol qoymaydi

Dasturchi: @Muhammad_3067
"""


async def activate_bot(message: types.Message):
    await bot.send_message(message.from_user.id, 'Bizning boshqaruvchi botimizga xush kelibsiz. Qoshimcha malumot olish uchun /help ni yozing', reply_markup=user_keyboards.button_case_user)

    # Записываем каждог пользователя который пользуется нашим ботом
    users_list = search.get_users_data()
    if users_list == '':
        search.add_user_data(message, users_list)
    else:
        search.add_user_data(message, users_list)



async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, HELP_TEXT)


async def product_read_last_five(message: types.Message):
    await sqlite_db.sql_read_last_five(message)


async def product_read_all(message: types.Message):
    await sqlite_db.sql_read_all(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(activate_bot, commands='start')
    dp.register_message_handler(help_command, commands='help')
    dp.register_message_handler(product_read_last_five, Text('Menu'))
    dp.register_message_handler(product_read_all, Text('Hamma maxsulotlar'))
