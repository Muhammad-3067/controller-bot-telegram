import uuid
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_file import bot
from keyboards import admin_keyboard
from database import sqlite_db, temporary_database
from cfgs import cfg

ID = None


class FSAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Проверка на админ, является ли пользователь админом если да тогда возвраoаем его id
async def admin_panel(message: types.Message):
    admins_data = await bot.get_chat_administrators(chat_id=cfg.CHANNEL_ID)
    admins_id_list = [x.user.id for x in admins_data]
    if message.from_user.id in admins_id_list:
        global ID
        ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Xush kelibsiz Admin', reply_markup=admin_keyboard.button_case_admin)
    await message.delete()


# Начало загрузки новых вещей в бот
async def activate_uploading(message: types.Message):
    if message.from_user.id == ID:
        await FSAdmin.photo.set()
        await bot.send_message(ID, 'Mahsulot rasmi', reply_markup=admin_keyboard.button_cancel_admin)


async def upload_photo_err(message: types.Message):
    await message.delete()
    return await bot.send_message(message.from_user.id, 'Iltimos rasim jonating')

async def upload_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSAdmin.next()
        await bot.send_message(ID, 'Mahsulot nomi', reply_markup=admin_keyboard.button_cancel_admin)


async def upload_name_err(message: types.Message):
    await message.delete()
    return await bot.send_message(message.from_user.id, 'Iltimos tovar nomini harflar bilan yozing')
    
async def upload_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSAdmin.next()
        await bot.send_message(ID, 'Mahsulot haqida', reply_markup=admin_keyboard.button_cancel_admin)


async def upload_description_err(message: types.Message):
    await message.delete()
    return await bot.send_message(message.from_user.id, 'Iltimos tovar nomini harflar bilan yozing')

async def upload_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSAdmin.next()
        await bot.send_message(ID, 'Mahsulot narxi', reply_markup=admin_keyboard.button_cancel_admin)


async def upload_price_err(message: types.Message):
    await message.delete()
    return await bot.send_message(message.from_user.id, 'Iltimos tovar narxini raqamlarda yozing')

async def upload_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = int(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()
        await bot.send_message(ID, 'Mahsulot bazaga muvofaqiyatli qo\'shildi', reply_markup=admin_keyboard.button_case_admin)
        await sqlite_db.sql_read_last()
        
        # Checking database if in database have more products than we want delete them
        sqlite_db.control_database()


# Добавления media_group 
async def send_message_media_group(message: types.Message):
    max_data = await temporary_database.max_quantity_media()
    if max_data > 0:
        return await message.answer("Bazada hali post qilinmagan tovarlar bor. Barcha tovarlar post qilib bo'linganidan so'ng biz sizga xabar beramiz")
    if message.from_user.id == ID:
        await message.answer('Ok now send media group', reply_markup=admin_keyboard.button_media_end_admin)
        cfg.UPLOADING = True

async def get_media_group(message: types.Message):
    max_data = await temporary_database.max_quantity_media()
    if max_data > 100:
        return await message.answer("Bazada joy to'ldi iltimos bir necha soatdan keyin harakat qilib ko'ring")
    if message.from_user.id == ID:
        if cfg.UPLOADING:
            data = {}
            data['media_photo'] = message.photo[0].file_id
            data['id'] = f"{uuid.uuid4()}"
            await temporary_database.sql_add_command(data)

async def end_uploading_media_group(message: types.Message):
    await message.answer('Tovarlar bazaga yuklandi.', reply_markup=admin_keyboard.button_case_admin)
    await temporary_database.read_temporarly(message.chat.id)
    cfg.UPLOADING = False


# Меню которая показывает последний 5 продукт
async def admin_read_last_five(message: types.Message):
    await sqlite_db.sql_admin_menu_five(message)

# Кнопка отмена загрузки нового продукта в базу данных
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await bot.send_message(ID, 'Yuklash bekor qilindi', reply_markup=admin_keyboard.button_case_admin)


# Удаления продуктов из база данных с помощью инлайн кнопки
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} Deleted.', show_alert=True)


def register_handlers_admin(dp: Dispatcher):

    dp.register_message_handler(admin_panel, commands=[
                                'admin'])
    dp.register_message_handler(
        cancel_handler, Text(equals='Bekor qilish', ignore_case=True), state='*')
    dp.register_message_handler(
        activate_uploading, Text(equals='Yuklash'), state=None)
    dp.register_message_handler(admin_read_last_five, Text(equals='Admin menu'))


    # get_media_group
    dp.register_message_handler(send_message_media_group, Text(equals='Rasmlar yuklash'))
    dp.register_message_handler(get_media_group, content_types=['photo'])
    dp.register_message_handler(end_uploading_media_group, Text(equals="To'xtatish"))


    # register для удаления продуктов из база данных
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))


    # Добавление новых продуктов в базу данных
    dp.register_message_handler(upload_photo_err, lambda message: not message.photo, state=FSAdmin.photo)
    dp.register_message_handler(upload_photo, content_types=[
                                'photo'], state=FSAdmin.photo)

    dp.register_message_handler(upload_name_err, lambda message: message.text.isdecimal(), state=FSAdmin.name)
    dp.register_message_handler(upload_name, state=FSAdmin.name)

    dp.register_message_handler(upload_description_err, lambda message: message.text.isdecimal(), state=FSAdmin.description)
    dp.register_message_handler(upload_description, state=FSAdmin.description)

    dp.register_message_handler(upload_price_err, lambda message: not message.text.isdecimal(), state=FSAdmin.price)
    dp.register_message_handler(upload_price, state=FSAdmin.price)
