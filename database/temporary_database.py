import sqlite3 as sq
import asyncio
from bot_file import bot
from cfgs import cfg
import random

media_text = """
Do'konimizga yangi tovarlar keldi narxlarni bilish uchun adminga murojaat qiling: @Muhammad_3067
"""

def sql_start():
    global base, cur
    base = sq.connect('temporary_database.db')
    cur = base.cursor()
    if base:
        print('temporary database connected Ok')
    base.execute(
        'CREATE TABLE IF NOT EXISTS media_photos(img TEXT PRIMARY KEY, unique_id TEXT)')
    base.commit()


async def sql_add_command(state):
    cur.execute('INSERT INTO media_photos VALUES(?, ?)', tuple(state.values()))
    base.commit()


async def read_temporarly(chat_id):
    data = cur.execute("SELECT * FROM media_photos ORDER BY rowid").fetchall()
    for media in data:
        random_num = random.randint(4, 10)
        random_num_in_sec = 60 * random_num
        await asyncio.sleep(random_num_in_sec)
        await bot.send_photo(cfg.CHANNEL_ID, media[0], media_text)

    
    await bot.send_message(chat_id, "Bazadagi barcha tovarlar post qilib bo'lindi. Yangi tovarlar joylashingiz mumkin")

    cur.execute("DELETE FROM media_photos;",)
    base.commit()

async def max_quantity_media():
    data = cur.execute("SELECT * FROM media_photos ORDER BY rowid")
    num_data = 0
    for media in data:
        num_data += 1
    return num_data
