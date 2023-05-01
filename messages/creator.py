from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards import creator_keyboard
from messages import search 

async def creator_command(message: types.Message):
    if message.from_user.id == 797678891:
        await message.answer(f'Sizni korganimdan xursandman {message.from_user.full_name}', reply_markup=creator_keyboard.creator_count_users)

async def count_users(message: types.Message):
    if message.from_user.id == 797678891:
        number_of_users = search.get_users_data()
        if number_of_users == '':
            await message.answer("Afsuski botda foydalanuvchilar hali mavjud emas")
        else:
            data_len = len(number_of_users)
            summ_of_users = 0
            for user in range(data_len):
                if user == 0:
                    summ_of_users += user+1
                summ_of_users += user
            await message.answer(f"Foydalanuvchilar soni: {summ_of_users}")

def register_handlers_creator(dp: Dispatcher):
    dp.register_message_handler(creator_command, commands='creatoredd1t')
    dp.register_message_handler(count_users, Text(equals="Foydalanuvchilar"))