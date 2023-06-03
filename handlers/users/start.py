import logging
import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message, ReplyKeyboardMarkup
from keyboards.default.main_menu import uz_main, en_main
from keyboards.inline.languages import language_btn
from data.config import CHANNELS
from loader import dp, db, bot
from states.main_state import Main
from .texts import language



# @dp.message_handler(content_types=types.ContentType.STICKER)
# async def handle_sticker(message: types.Message):
#     sticker_id = message.sticker.file_id
#     print(f"Sticker ID: {sticker_id}")


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: Message, state: FSMContext):
    sticker_id = 'CAACAgIAAxkBAAMEZHhjRryv3gABQQel6wS0oIKy0u_HAAIBAQACVp29CiK-nw64wuY0LwQ'
    is_user = await db.select_user(message.from_user.id)
    if is_user:
        lang = await db.getUser_lang(message.from_user.id)
        if lang == 'uz':
        # set language
            await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
            await Main.main_menu.set()
        elif lang == 'en':
            await message.answer("🏡 Main menu", reply_markup=en_main())
            await Main.main_menu.set()

    else:
        if is_user is None:
            try:
                user = await db.add_user(telegram_id=message.from_user.id,
                                         full_name=message.from_user.full_name,
                                         username=message.from_user.username,
                                         )

            except asyncpg.exceptions.UniqueViolationError:
                pass
            await bot.send_sticker(chat_id=message.chat.id, sticker=sticker_id)
            await message.answer(language(), reply_markup=language_btn())
            await state.set_state("get_lang")


@dp.callback_query_handler(text_contains='til', state="get_lang")
async def setLang(call: CallbackQuery, state: FSMContext):
    lang = call.data.rsplit(':')
    til = lang[1]
    await call.message.delete()
    await db.update_user_language(call.from_user.id, til)
    if til == 'uz':
        await call.message.answer("Iltimos, to'liq ismingizni kiriting: ⬇️\n\nMisol: <b>Aziz Azizov</b>", reply_markup=ReplyKeyboardRemove())
        await state.set_state("getname")
    elif til == 'en':
        await call.message.answer("Please enter your fullname: ⬇️\n\nExample: <b>Aziz Azizov</b>", reply_markup=ReplyKeyboardRemove())
        await state.set_state("getname")




@dp.message_handler(state='getname')
async def get_name(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    name = message.text
    if len(name.split()) == 2:
        await db.update_user_name(message.from_user.id, name)
        if lang == 'uz':
            await message.answer("✅ Siz ro'yxatdan muvaffaqiyatli o'tdingiz!")
            await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
            await Main.main_menu.set()
        elif lang == 'en':
            await message.answer('✅ You have successfully registered!')
            await message.answer("🏡 Main menu", reply_markup=en_main())
            await Main.main_menu.set()

    else:
        if lang == 'uz':
           await message.answer("To'liq ismingizni qayta kiriting!\n\nMisol: <b>Aziz Azizov</b>")
           return
        elif lang == 'en':
            await message.answer('Re-enter your full name!\n\nExample: <b>Aziz Azizov</b>')