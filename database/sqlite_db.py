import sqlite3 as sq
from bot_file import bot
from cfgs import cfg
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.price_devider import sort_price

# Создание файла база данных
def sql_start():
    global base, cur
    base = sq.connect('group_helper.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()

        
    
# Добавления новых товаров в базу данных
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)',
                    tuple(data.values()))
        base.commit()

# Кантрол база данных если в базе данных будут больше 10 товаров тогда удаляется более старые товары
def control_database():
    items = cur.execute('SELECT * FROM menu ORDER BY rowid').fetchall()
    if len(items) > 10:
        print("yes")
        data = cur.execute('SELECT * FROM menu ORDER BY rowid').fetchone()
        cur.execute('DELETE FROM menu WHERE name == ?', (data[1],))
        base.commit()

    
# Отправляет последный добавленный продукт в группу
async def sql_read_last():
    item = cur.execute('SELECT * FROM menu').fetchall()[-1]
    await bot.send_photo(cfg.CHANNEL_ID, item[0], f'📄Nomi: {item[1]}\n📝Tovar: {item[2]}\n💰Narxi: {sort_price(item[3])} so\'m')

# Это кнопка которая показывает последный 5 продукт для пользователей
async def sql_read_last_five(message):
    data = cur.execute('SELECT * FROM menu ORDER BY rowid DESC').fetchmany(5)
    data.reverse()

    if len(data) <= 0:
        return await bot.send_message(message.from_user.id, "Bazaga hali yangi tovar qoshilmadi. Iltimos keyinroq harakat qilib ko'ring")
    for ret in data:
        await bot.send_photo(message.from_user.id, ret[0], f'📄Nomi: {ret[1]}\n📝Tovar: {ret[2]}\n💰Narxi: {sort_price(ret[3])} so\'m')

# Это кнопка которая показывает всех продуктов для пользователей
async def sql_read_all(message):
    data = cur.execute('SELECT * FROM menu ORDER BY rowid DESC').fetchall()
    data.reverse()
    
    if len(data) <= 0:
        return await bot.send_message(message.from_user.id, "Bazaga hali yangi tovar qoshilmadi. Iltimos keyinroq harakat qilib ko'ring")
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'📄Nomi: {ret[1]}\n📝Tovar: {ret[2]}\n💰Narxi: {sort_price(ret[3])} so\'m')


# Удаления продукта из база данных
async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()



# Это кнопка которая показывает последный 5 продукт для админа с возможностью удаление
async def sql_admin_menu_five(message):
    data = cur.execute('SELECT * FROM menu ORDER BY rowid DESC').fetchmany(5)
    data.reverse()

    if len(data) <= 0:
        return await bot.send_message(message.from_user.id, "Bazaga hali yangi tovar qoshilmadi. Iltimos keyinroq harakat qilib ko'ring")
    for ret in data:
        await bot.send_photo(message.from_user.id, ret[0], f'📄Nomi: {ret[1]}\n📝Tovar: {ret[2]}\n💰Narxi: {sort_price(ret[3])} so\'m', \
                             reply_markup=InlineKeyboardMarkup().
                                    add(InlineKeyboardButton(f'Delete {ret[1]}', callback_data=f'del {ret[1]}')))
        
# Это кнопка которая показывает всех продуктов для админа с возможностью удаление
async def sql_admin_read_all(message):
    data = cur.execute('SELECT * FROM menu ORDER BY rowid DESC').fetchall()
    data.reverse()
    
    if len(data) <= 0:
        return await bot.send_message(message.from_user.id, "Bazaga hali yangi tovar qoshilmadi. Iltimos keyinroq harakat qilib ko'ring")
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'📄Nomi: {ret[1]}\n📝Tovar: {ret[2]}\n💰Narxi: {sort_price(ret[3])} so\'m', \
                             reply_markup=InlineKeyboardMarkup().
                                    add(InlineKeyboardButton(f'Delete {ret[1]}', callback_data=f'del {ret[1]}')))
        