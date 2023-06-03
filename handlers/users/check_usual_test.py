from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, CallbackQuery, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.types.message import Message
import re
from keyboards.default.main_menu import en_main, uz_main
from keyboards.inline.rating import rating_button_uz, rating_button_en, end_test_en, end_test_uz
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from states.main_state import Main

from datetime import date, datetime
from pytz import timezone
from .texts import after_test_high, after_test_high_en, send_to_creator, status, send_to_creator_en

check_btn = ['🔑 Test tekshirish', '🔑 Check test']
uz_link = 'https://telegra.ph/Test-tekshirish-yoriqnomasi-06-01'
en_link = 'https://telegra.ph/Test-check-instructions-06-01'


@dp.message_handler(text=check_btn, state=Main.main_menu)
async def check_fstep(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        home_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        home_btn.add("🏡 Bosh menyu")
        await message.answer("Test tekshirish yo'riqnomasi bilan <b>diqqat bilan tanishib chiqing!</b>")
        await message.answer(uz_link)
        await message.answer("Test javoblarini kiritishingiz mumkin 🔽", reply_markup=home_btn)
        await state.set_state("next_step1")

    elif lang == 'en':
        home_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        home_btn.add("🏡 Main menu")
        await message.answer("Please <b>carefully read the inspection instructions of cheking the test!</b>")
        await message.answer(en_link)
        await message.answer("You can enter test answers 🔽", reply_markup=home_btn)
        await state.set_state("next_step1")


@dp.message_handler(state='next_step1')
async def next_steep(message: Message, state: FSMContext):
    errors = 0
    errors_list = list()
    lang = await db.getUser_lang(message.from_user.id)
    value = message.text

    if lang == 'uz':
        if value == '🏡 Bosh menyu':
            await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
            await Main.main_menu.set()
        else:
            if "*" in value:
                where_is_star = value.find("*")
                where_is_star = int(where_is_star)
                where_is_star += 1

                user_answers = value[where_is_star:]
                user_answers = user_answers.lower()
                if user_answers.isdigit():
                    await message.answer(uz_link, reply_markup=ReplyKeyboardRemove())
                    return
                else:
                    pass

                where_is_star -= 1
                test_id = value[:where_is_star]

                is_test_yes = await db.get_test_by_id(test_id)
                if is_test_yes:
                    test_id = int(test_id)
                    test_type = await db.get_test_type(test_id)
                    print(test_type)
                    if test_type == "usual":
                        is_Done_before = await db.check_is_done(test_id, message.from_user.id)

                        if is_Done_before is None:
                            test_status = await db.get_test_status(test_id)
                            if test_status == 0:
                                await message.answer(status())
                                await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                                await Main.main_menu.set()
                            elif test_status == 1:
                                correct_answer = await db.get_test_answers(test_id)  # correct answers
                                user_answers = re.sub('[^a-zA-Z]+', '', user_answers)  # user answers
                                len1 = await db.get_test_length(test_id)
                                len2 = len(user_answers)
                                date_t = date.today()
                                date_t = str(date_t)

                                if len1 == len2:

                                    await db.add_done_test(test_id, message.from_user.id, date_t)

                                    for x, y in zip(correct_answer, user_answers):
                                        if x == y:
                                            pass
                                        else:
                                            errors += 1

                                    name = await db.getUser_name(message.from_user.id)
                                    subject = await db.get_test_name(test_id)
                                    user_id = str(message.from_user.id)
                                    test_code = test_id
                                    questionLength = len(correct_answer)
                                    userAnswers = len(correct_answer) - errors
                                    percent = userAnswers / questionLength * 100
                                    percent = round(percent)
                                    test_id = str(test_id)
                                    time_format = '%Y-%m-%d %H:%M:%S'
                                    formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
                                    datetime_object = datetime.strptime(formatted_now, "%Y-%m-%d %H:%M:%S")

                                    await db.add_rating(test_id, user_id, name, percent, datetime_object, "usual")
                                    await message.answer(
                                        after_test_high(message.from_user.username, name, subject, test_code,
                                                        questionLength,
                                                        userAnswers, percent, formatted_now),
                                        disable_web_page_preview=True, reply_markup=rating_button_uz())
                                    await message.answer(
                                        "📊 <b>Reyting</b> test yakunlanganidan so'ng, sizga <i>avtomatik tarzda yuboriladi!</i>")
                                    await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                                    await Main.main_menu.set()

                                    for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answer),
                                                                                      start=1):
                                        if user_answer != correct_answer:
                                            await db.add_errors(user_id, test_id, i)

                                    creator_id = await db.get_test_creator(test_id)
                                    await bot.send_message(chat_id=creator_id,
                                                           text=send_to_creator(name, subject, test_id, questionLength,
                                                                                errors, message.from_user.username),
                                                           reply_markup=end_test_uz(test_id),
                                                           disable_web_page_preview=True)
                                    await Main.main_menu.set()
                                else:
                                    await message.answer(
                                        f"❗️ <b>{test_id}</b>-sonli testning {len1}-ta savoli mavjud!\n\n"
                                        f"<i>Siz esa {len2}-ta javob yubordingiz. Iltimos, qayta yuboring!!!</i>")
                                    return

                        else:
                            await message.answer("Siz bu testni avval yechgansiz! Qayta javob berish mumkun emas!")
                            await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                            await Main.main_menu.set()

        # English language
    elif lang == 'en':
        if value == '🏡 Main menu':
            await message.answer("🏡 Main menu", reply_markup=en_main())
            await Main.main_menu.set()
        else:
            if "*" in value:
                where_is_star = value.find("*")
                where_is_star = int(where_is_star)
                where_is_star += 1

                user_answers = value[where_is_star:]
                user_answers = user_answers.lower()
                if user_answers.isdigit():
                    await message.answer(uz_link, reply_markup=ReplyKeyboardRemove())
                    return
                else:
                    pass

                where_is_star -= 1
                test_id = value[:where_is_star]

                is_test_yes = await db.get_test_by_id(test_id)
                if is_test_yes:
                    test_id = int(test_id)
                    test_type = await db.get_test_type(test_id)
                    if test_type == "usual":
                        is_Done_before = await db.check_is_done(test_id, message.from_user.id)

                        if is_Done_before is None:
                            test_status = await db.get_test_status(test_id)
                            if test_status == 0:
                                await message.answer(status())
                                await message.answer("🏡 Main menu", reply_markup=en_main())
                                await Main.main_menu.set()
                            elif test_status == 1:
                                correct_answer = await db.get_test_answers(test_id)  # correct answers
                                user_answers = re.sub('[^a-zA-Z]+', '', user_answers)  # user answers
                                len1 = await db.get_test_length(test_id)
                                len2 = len(user_answers)
                                date_t = date.today()
                                date_t = str(date_t)

                                if len1 == len2:

                                    await db.add_done_test(test_id, message.from_user.id, date_t)

                                    for x, y in zip(correct_answer, user_answers):
                                        if x == y:
                                            pass
                                        else:
                                            errors += 1

                                    name = await db.getUser_name(message.from_user.id)
                                    subject = await db.get_test_name(test_id)
                                    user_id = str(message.from_user.id)
                                    test_code = test_id
                                    questionLength = len(correct_answer)
                                    userAnswers = len(correct_answer) - errors
                                    percent = userAnswers / questionLength * 100
                                    percent = round(percent)
                                    time_format = '%Y-%m-%d %H:%M:%S'
                                    test_id = str(test_id)
                                    formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
                                    datetime_object = datetime.strptime(formatted_now, "%Y-%m-%d %H:%M:%S")

                                    await db.add_rating(test_id, user_id, name, percent, datetime_object, "usual")
                                    await message.answer(
                                        after_test_high_en(message.from_user.username, name, subject, test_code,
                                                           questionLength,
                                                           userAnswers, percent, formatted_now),
                                        disable_web_page_preview=True, reply_markup=rating_button_en())
                                    await message.answer(
                                        "📊 <b>Rating</b> will be sent to you <i>automatically after the test is completed!</i>")
                                    await message.answer("🏡 Main menu", reply_markup=en_main())
                                    await Main.main_menu.set()

                                    creator_id = await db.get_test_creator(test_id)
                                    await bot.send_message(chat_id=creator_id,
                                                           text=send_to_creator_en(name, subject, test_id,
                                                                                   questionLength, errors,
                                                                                   message.from_user.username),
                                                           reply_markup=end_test_en(test_id),
                                                           disable_web_page_preview=True)
                                    await Main.main_menu.set()

                                    for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answer),
                                                                                      start=1):
                                        if user_answer != correct_answer:
                                            await db.add_errors(user_id, test_id, i)



                                else:
                                    await message.answer(f"❗️ Test <b>{test_id}</b> has {len1} questions!\n\n"
                                                         f"<i>And you sent a reply to {len2}. Please resend!!!</i>")
                                    return

                        else:
                            await message.answer("You've solved this test before! Can't reply back!")
                            await message.answer("🏡 Main menu", reply_markup=en_main())
                            await Main.main_menu.set()
                    else:
                        pass
