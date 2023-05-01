from datetime import timedelta
from aiogram import types, Dispatcher
from bot_file import bot
from cfgs import cfg

async def somebody_added(message: types.Message):
    user_data = await bot.get_chat_member(chat_id=cfg.CHANNEL_ID, user_id=message.from_user.id)
    user_status = user_data.status

    for user in message.new_chat_members:

        # Этот delete() что-бы удалить смс кто-то каго-то добавил
        await message.delete()

        if user.is_bot == False:
            return await message.answer(f"Xush kelibsiz, <b>{user.full_name}</b>", parse_mode='HTML')
        if user_status == 'member':
            await bot.ban_chat_member(chat_id=message.chat.id, user_id=user.id, until_date=timedelta(seconds=29))
            return await message.answer(f"<b>{message.from_user.full_name}</b>, bu guruhga admin ruxsatisiz bot qoshish mumkin emas, shuning uchun <b>{user.full_name}</b> ban qilindi", parse_mode='HTML')
        return await message.answer(f'Admin guruhga <b><i>{user.full_name}</i></b> bot ni qoshdi, guruhni boshqarish uchun', parse_mode='HTML')
    


async def check_text_toUrl(message: types.Message):
    user_data = await bot.get_chat_member(chat_id=cfg.CHANNEL_ID, user_id=message.from_user.id)
    user_status = user_data.status


    if user_status == 'member':
        if 'https://' in message.text.lower() or 'http://' in message.text.lower():
            await message.answer(f'{message.from_user.full_name}, Bu guruhda silkali sms jonatish taqiqlangan')
            await message.delete()
        elif '@' in message.text.lower():
            await message.answer(f'{message.from_user.full_name}, Bu guruhda silkali sms jonatish taqiqlangan')
            await message.delete()
        


def register_handlers_group(dp: Dispatcher):
    dp.register_message_handler(
        somebody_added, content_types=types.ContentType.NEW_CHAT_MEMBERS)

    dp.register_message_handler(
        check_text_toUrl)
    