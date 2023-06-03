from loader import dp, db, bot  
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from keyboards.default.main_menu import uz_main, en_main
from states.main_state import Main
from keyboards.inline.rating import reyting_en, reyting_uz
from .texts import test_info_en, test_info_uz




my_text = ['📑 Mening testlarim', '📑 My tests']
@dp.message_handler(text=my_text, state=Main.main_menu)
async def showMyTests(message: Message, state: FSMContext):
    buttons_markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    buttons_list = []
    lang = await db.getUser_lang(message.from_user.id)
    tests = await db.get_test_by_creator(message.from_user.id)
    if len(tests) == 0:
        if lang == 'uz':
            await message.answer('😕 Siz xali test yaratmagansiz!')
            await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
            await Main.main_menu.set()
        elif lang == 'en':
            await message.answer("😕 You haven't created a test yet!")
            await message.answer("🏡 Main menu", reply_markup=en_main())
            await Main.main_menu.set()
    else:
        for test_id, date in tests:
            joined_name = f"{test_id} - {date}"  # Join the test name and date
            buttons_list.append(joined_name)
        
        buttons_markup.add(*buttons_list)
        if lang == 'uz':
            await message.answer('Testlaringiz: ', reply_markup=buttons_markup)
            await state.set_state('test_info')
        elif lang == 'en':
            await message.answer('Your tests: ', reply_markup=buttons_markup)
            await state.set_state('test_info')

        
    



@dp.message_handler(state='test_info')
async def show_info(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    info = message.text.split(" ")
    test_id = info[0]

    lentgh = await db.get_test_length(test_id)
    subject = await db.get_test_name(test_id)
    participants = await db.count_participants(test_id) 
    date = await db.get_test_date(test_id)
    for j in participants:
        p = j[0]
    if lang == 'uz':
        a = test_info_uz(subject, test_id, lentgh, p, date)
        await message.answer(a, reply_markup=reyting_uz(test_id))
        await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
        await Main.main_menu.set()
    elif lang == 'en':
        await message.answer(test_info_en(subject, test_id, lentgh, p, date), reply_markup=reyting_en(test_id))
        await message.answer("🏡 Main menu", reply_markup=en_main())
        await Main.main_menu.set()



@dp.callback_query_handler(text_contains='rating', state=Main.main_menu)
async def show_ratingSSS(call: CallbackQuery, state: FSMContext):
    lang = await db.getUser_lang(call.from_user.id)
    data = call.data.rsplit(':')
    test_id = data[1]
    subject = await db.get_test_name(test_id)
    if lang == 'uz':
        rating = await db.show_rating_by_user(test_id)
        show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
        i = 1
        for user in rating:
            emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
            show_rating += "{0}) {1}{2} - {3} %\n".format(i, user['full_name'], emoji, user['ball'])
            i += 1
        await call.message.answer(show_rating, reply_markup=uz_main())
        await Main.main_menu.set()
        
    elif lang == 'en':
        rating = await db.show_rating_by_user(test_id)
        show_rating = f"📕 Subject: <b>{subject}</b>\n🎛 Test code: <b>{test_id}</b>\n\nRATING by test with code {test_id}⬇️\n\n"
        i = 1
        for user in rating:
            emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
            show_rating += "{0}) {1}{2} - {3} %\n".format(i, user['full_name'], emoji, user['ball'])
            i += 1
        await call.message.answer(show_rating, reply_markup=en_main())
        await Main.main_menu.set()

    
    

