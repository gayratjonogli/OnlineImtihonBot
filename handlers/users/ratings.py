from loader import dp, db, bot
from aiogram.types import Message
from keyboards.default.main_menu import uz_main, en_main
from aiogram.dispatcher import FSMContext
from states.main_state import Main


rating_btn = ["📊 Reyting ko'rish", "📊 Ratings"]
@dp.message_handler(text=rating_btn, state=Main.main_menu)
async def showRating(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        await message.answer("Test-ID kiriting: ⬇️")
        await state.set_state('get_id')
    elif lang == 'en':
        await message.answer('Enter Test-ID')
        await state.set_state('get_id')


@dp.message_handler(state='get_id')
async def check_id(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    test_id = message.text
    name = await db.getUser_name(message.from_user.id)
    if test_id.isdigit():
        is_test = await db.get_test_by_id(test_id)
        if is_test:
            subject = await db.get_test_name(test_id)
            test_status = await db.get_test_status(test_id)
            if test_status == 0:
                rating = await db.show_rating_by_user(test_id)
                if lang == 'uz':
                    show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
                    i = 1
                    for user in rating:
                        emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
                        show_rating += "{0}) {1}{2} - {3} foiz\n".format(i, name, emoji, user['ball'])
                        i += 1


                    show_rating += "\n🤖 Bot Abdulaziz Madaminov (@abdulaziz_madaminov) tomonidan tayyorlandi."
                    await message.answer(show_rating)
                    await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                    await Main.main_menu.set()
                
                elif lang == 'en':
                    show_rating = f"📕 Subject: <b>{subject}</b>\n🎛 Test code: <b>{test_id}</b>\n\nRATING by test with code {test_id}⬇️\n\n"
                    i = 1
                    for user in rating:
                        emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
                        show_rating += "{0}) {1}{2} - {3} %\n".format(i, name, emoji, user['ball'])
                        i += 1


                    show_rating += "\n🤖 The bot was created by Abdulaziz Madaminov (@abdulaziz_madaminov)."
                    await message.answer(show_rating)
                    await message.answer("🏡 Main menu", reply_markup=en_main())
                    await Main.main_menu.set()
            elif test_status == 1:
                if lang == 'uz':
                    await message.answer("❌ Test yakunlanmagani sababli, reytingni ko'ra olmaysiz!")
                    await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                    await Main.main_menu.set()

                elif lang == 'en':
                    await message.answer("❌ Since the test is not completed, you cannot see the rating!")
                    await message.answer("🏡 Main menu", reply_markup=en_main())
                    await Main.main_menu.set()

        else:
            if lang == 'uz':
                await message.answer(f'🤷‍♂ <b>{test_id}</b>-sonli test bazadan topilmadi!\n\nTekshirib, qayta kiriting!')
                return
            elif lang == 'en':
                await message.answer(f'🤷‍♂ Test with <b>{test_id}-ID</b> was not found in the database!\n\nCheck and re-enter!')
                return
            
    else:
        if lang == 'uz':
            await message.answer('😡 Xato kiritingiz!\nTest-ID faqat raqamlardan iborat!\n\nQayta kiriting!')
            return
        elif lang == 'en':
            await message.answer('😡 Typing error!\nTest-ID is only numbers!\n\nRetype!')
            return
