from loader import dp, db, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from states.main_state import Main
from keyboards.default.main_menu import uz_main, en_main
from keyboards.inline.rating import see_errors_uz, see_errors_en



@dp.callback_query_handler(text_contains='creator', state=Main.main_menu)
async def endthetest(call: CallbackQuery, state: FSMContext):
    lang = await db.getUser_lang(call.from_user.id)
    data = call.data.rsplit(':')
    test_id = data[2]
    action = data[1]
    subject = await db.get_test_name(test_id)
    if action == 'rating':
        if lang == 'uz':
            rating = await db.show_rating_by_user(test_id)
            show_rating = f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
            i = 1
            for user in rating:
                emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
                show_rating += "{0}) {1}{2} - {3} %\n".format(i, user['full_name'], emoji, user['ball'])
                i += 1
            await call.message.answer(show_rating)
        
        elif lang == 'en':
            rating = await db.show_rating_by_user(test_id)
            show_rating = f"📕 Subject: <b>{subject}</b>\n🎛 Test code: <b>{test_id}</b>\n\nRATING by test with code {test_id}⬇️\n\n"
            i = 1
            for user in rating:
                emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
                show_rating += "{0}) {1}{2} - {3} %\n".format(i, user['full_name'], emoji, user['ball'])
                i += 1
            await call.message.answer(show_rating)


    elif action == 'end_test':
        test_users_list = list()
        test_status = await db.get_test_status(test_id)
        if test_status == 0:
            if lang == 'uz':
                await call.message.answer("Test allaqachon yakunlanib bo'lgan!\nQayta yakunlash mumkin emas!")
                await call.message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                await Main.main_menu.set()
            elif lang == 'en':
                await call.message.answer("The test has already been completed!\nCannot be completed again!")
                await call.message.answer("🏡 Main menu", reply_markup=en_main())
                await Main.main_menu.set()

        else:
            await db.update_test_status(test_id, 0)
            if lang == 'uz':
                await call.message.answer("Test muvaffaqiyatli yakunlandi!")
            elif lang == 'en':
                await call.message.answer("Test completed successfully!")

            test_users = await db.get_test_users(test_id)
            for i in test_users:
                test_users_list.append(i[0])

            for users in test_users_list:
                if lang == 'uz':
                    rating = await db.show_rating_by_user(test_id)
                    show_rating = "<b>TEST JAVOBLARI REYTINGI E'LON QILINDI!</b>\n\n"
                    show_rating += f"📕 Fan: <b>{subject}</b>\n🎛 Test kodi: <b>{test_id}</b>\n\n{test_id}-kodli test bo'yicha REYTING⬇️\n\n"
                    i = 1
                    for user in rating:
                        emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
                        show_rating += "{0}) {1}{2} - {3} foiz\n".format(i, user['full_name'], emoji, user['ball'])
                        i += 1

                    await bot.send_message(chat_id=users, text=show_rating, reply_markup=see_errors_uz(users, test_id))
                    await Main.main_menu.set()
                elif lang == 'en':
                    rating = await db.show_rating_by_user(test_id)
                    show_rating = "<b>TEST ANSWER RANKINGS ANNOUNCED!</b>\n\n"
                    show_rating += f"📕 Subject: <b>{subject}</b>\n🎛 Test code: <b>{test_id}</b>\n\nRATING by test with code {test_id}⬇️\n\n"
                    i = 1
                    for user in rating:
                        emoji = "🥇 " if i == 1 else ""  # Add the 🥇 emoji only for the first user
                        show_rating += "{0}) {1}{2} - {3} %\n".format(i, user['full_name'], emoji, user['ball'])
                        i += 1

                    await bot.send_message(chat_id=users, text=show_rating, reply_markup=see_errors_en(users, test_id))
        
                    await Main.main_menu.set()




@dp.callback_query_handler(text_contains='error', state=Main.main_menu)
async def get_errors(call: CallbackQuery, state: FSMContext):
    lang = await db.getUser_lang(call.from_user.id)
    data =  call.data.rsplit(':')
    user_id = data[1]
    test_id = data[2]
    user_errors = list()

    errors = await db.get_user_errors(user_id, test_id)
    if lang == 'uz':
        if len(errors) == 0:
            await call.message.answer("<b>🥳 Tabriklaymiz!</b>\n\nSizda hech qanday xatolar mavjud emas!")
            await Main.main_menu.set()
        else:
            for error in errors:
                if error[0] != '':
                    user_errors.append(error[0])

            if len(user_errors) > 0:
                error_message = f"<b>{test_id}</b>-kodli test bo'yicha Sizning xatolaringiz:\n\n"
            for error in user_errors:
                error_message += f"❌ <b>{error}</b>- savol\n"
        
            await call.message.answer(error_message)
            await Main.main_menu.set()
    
    elif lang == 'en':
        if len(errors) == 0:
            await call.message.answer("<b>🥳 Congratulations!</b>\n\nYou have no errors!")
            await Main.main_menu.set()
        else:
            for error in errors:
                if error[0] != '':
                    user_errors.append(error[0])

            if len(user_errors) > 0:
                error_message = f"Your errors on the test code <b>{test_id}</b>:\n\n"
            for error in user_errors:
                error_message += f"❌ Question number - <b>{error}</b>\n"
        
            await call.message.answer(error_message)
            await Main.main_menu.set()
        
        


    

   