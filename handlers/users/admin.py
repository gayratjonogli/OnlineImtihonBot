from loader import db, dp, bot
from aiogram.types import Message
from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from states.main_state import Main


@dp.message_handler(chat_id=ADMINS,commands=['count'], state="*")
async def count_user(msg: Message, state: FSMContext):
    users = await db.count_users()
    await msg.answer(f"Botdan {users}-kishi ro'yxatdan o'tgan!")
    await Main.main_menu.set()


    
@dp.message_handler(chat_id=ADMINS,commands=['test'], state="*")
async def count_user(msg: Message, state: FSMContext):
    test = await db.count_test()
    await msg.answer(f"Botda {test}-ta test yaratilgan!")
    await Main.main_menu.set()


    