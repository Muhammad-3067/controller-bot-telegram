# import logging
from aiogram.utils import executor
# from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot_file import dp
from messages import group_message, admin_message, client_message, creator
from database import sqlite_db, temporary_database

# webhook settings
# WEBHOOK_HOST = 'https://redd1t.alwaysdata.net'
# WEBHOOK_PATH = ''
# WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
# WEBAPP_HOST = 'localhost'  # or ip
# WEBAPP_PORT = 5000

# logging.basicConfig(level=logging.INFO)

# dp.middleware.setup(LoggingMiddleware())


async def on_startup(_):
    # await bot.set_webhook(WEBHOOK_URL)
    sqlite_db.sql_start()
    temporary_database.sql_start()
    # insert code here to run it after start


# async def on_shutdown(dp):
#     logging.warning('Shutting down..')

#     # insert code here to run it before shutdown

#     # Remove webhook (not acceptable in some cases)
#     await bot.delete_webhook()

#     # Close DB connection (if used)
#     await dp.storage.close()
#     await dp.storage.wait_closed()

#     logging.warning('Bye!')

client_message.register_handlers_client(dp)
admin_message.register_handlers_admin(dp)
creator.register_handlers_creator(dp)
group_message.register_handlers_group(dp)

if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        # webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        # on_shutdown=on_shutdown,
        skip_updates=True,
        # host=WEBAPP_HOST,
        # port=WEBAPP_PORT,
    )