from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from loader import db, dp
from states.main_state import Main
from aiogram.dispatcher import FSMContext
from .texts import show_infor_uz, show_infor_en, show_infor_updated_uz, show_infor_updated_en
from keyboards.default.main_menu import change_name_uz, change_name_en, uz_main, en_main


t_btn = ["📁 Mening ma'lumotlarim", "📁 My information"]

@dp.message_handler(text=t_btn, state=Main.main_menu)
async def show_info(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    name = await db.getUser_name(message.from_user.id)
    if lang == 'uz':
        await message.answer(show_infor_uz(name), reply_markup=change_name_uz())
        await state.set_state("change_info")
    elif lang == 'en':
        await message.answer(show_infor_en(name), reply_markup=change_name_en())
        await state.set_state("change_info")



this_btn = ["🔀 Ismni o'zgartirish", "🔀 Change name", "🏡 Bosh menyu", "🏡 Main menu"]

@dp.message_handler(text=this_btn, state="change_info")
async def change_them(message: Message, state: FSMContext):
    option = message.text
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        if option == this_btn[2]:
            await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
            await Main.main_menu.set()
        elif option == this_btn[0]:
            await message.answer("Iltimos, ismingizni kiriting:\n\nMisol: <b>Aziz Azizov</b>")
            await state.set_state("cname")
    
    elif lang == 'en':
        if option == this_btn[3]:
            await message.answer("🏡 Main menu", reply_markup=en_main())
            await Main.main_menu.set()
        elif option == this_btn[1]:
            await message.answer("Please enter your name:\n\nExample: <b>Aziz Azizov</b>")
            await state.set_state("cname")
   


@dp.message_handler(state="cname")
async def change_name(message: Message, state: FSMContext):
    name = message.text
    lang = await db.getUser_lang(message.from_user.id)
    await db.update_user_name(message.from_user.id, name)
    name = await db.getUser_name(message.from_user.id)
    if lang == 'uz':
        await message.answer(show_infor_updated_uz(name), reply_markup=change_name_uz())
        await state.set_state("change_info")

    if lang == 'en':
        await message.answer(show_infor_updated_en(name), reply_markup=change_name_en())
        await state.set_state("change_info")



