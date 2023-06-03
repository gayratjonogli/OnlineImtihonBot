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

@dp.message_handler(chat_id=ADMINS, commands=['ad'], state="*")
async def send_add(message: Message, state: FSMContext):
    await message.answer('Xabarni kiriting:')
    await state.set_state('get_ad')

@dp.message_handler(content_types=['text'],state='get_ad')
async def get_addd(message: Message, state: FSMContext):
    ad = message.text
    users = await db.send_ad_get()
    for user in users:
        await asyncio.sleep(0.3)
        await bot.send_message(chat_id=user[0], text=ad, parse_mode='markdown')

    await message.answer("✅ Xabar muvvafaqiyatli yuborildi!")


@dp.message_handler(content_types=['photo'], state="get_ad")
async def sendBigPhoto(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    caption = message.caption

    users = await db.send_ad_get()
    for user in users:
        await asyncio.sleep(0.3)
        await bot.send_photo(chat_id=user[0], photo=photo, caption=caption, parse_mode="markdown")

    await message.answer("✅ Xabar muvvafaqiyatli yuborildi!")
    
    
