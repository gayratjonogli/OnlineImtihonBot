from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await db.create()
    #await db.drop_users()
    #await db.delete_done_test()
    #await db.drop_test()
    #await db.delete_table_rating()
    await db.create_table_test()
    await db.create_table_users()
    await db.create_table_done_test()
    await db.create_table_rating()
    await db.create_table_errors()
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
