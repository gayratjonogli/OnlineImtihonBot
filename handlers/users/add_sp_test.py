from loader import dp, db, bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from keyboards.default.main_menu import uz_main, en_main
import random
import re
from states.main_state import Main
from datetime import date, datetime
from pytz import timezone
from .texts import bazaga_qoshildi_en_pm, bazaga_qoshildi_uz_pm, bazaga_qoshildi_uz_a, bazaga_qoshildi_en_a


uz_link_pm = 'https://telegra.ph/Prezident-maktab-testlarini-qoshish-yoriqnomasi-06-03'
en_link_pm = 'https://telegra.ph/Instructions-for-adding-Presidential-School-tests-06-03'


uz_link_a = 'https://telegra.ph/Abiturient-testlari-qoshish-yoriqnomasi-06-03'
en_link_a = 'https://telegra.ph/Instructions-for-adding-Abiturient-tests-06-03'


@dp.message_handler(commands=['prezident_school'], state="*")
async def redirect_pm(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        await message.answer("Test qo'shish yo'riqnomasi bilan <b>diqqat bilan tanishib chiqing!</b>")
        await message.answer(uz_link_pm)
        await message.answer('Kiriting: ⬇️')
        await state.set_state('getPMQuestions')
    elif lang == 'en':
        await message.answer('Please read <b>carefully!</b> the instructions for adding a test')
        await message.answer(en_link_pm)
        await message.answer('Enter: ⬇️')
        await state.set_state('getPMQuestions')


@dp.message_handler(commands=['abiturient'], state="*")
async def redirect_pm(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    if lang == 'uz':
        await message.answer("Test qo'shish yo'riqnomasi bilan <b>diqqat bilan tanishib chiqing!</b>")
        await message.answer(uz_link_a)
        await message.answer('Kiriting: ⬇️')
        await state.set_state('getABQuestions')
    elif lang == 'en':
        await message.answer('Please read <b>carefully!</b> the instructions for adding a test')
        await message.answer(en_link_a)
        await message.answer('Enter: ⬇️')
        await state.set_state('getABQuestions')


@dp.message_handler(state="getPMQuestions")
async def addPMQ(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    test_id = random.randint(0, 999999)
    full_answer = message.text
    time_format = '%d.%m.%Y'
    formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
    if "*" in full_answer:
        where_is_star = full_answer.find("*")
        where_is_star = int(where_is_star)
        where_is_star += 1
        answers = full_answer[where_is_star:]
        where_is_star -= 1
        subject = full_answer[:where_is_star]
        user_answers = re.sub('[^a-zA-Z]+', '', answers)
        user_answers = user_answers.lower()
        length = len(user_answers)
        if answers.isdigit():   
            if lang == 'uz':
                await message.answer(uz_link_pm, reply_markup=ReplyKeyboardRemove())
                await message.answer('Kiriting: ⬇️')
                return
            elif lang == 'en':
                await message.answer(en_link_pm, reply_markup=ReplyKeyboardRemove())
                await message.answer('Enter: ⬇️')
                return

        #
        if len(user_answers) == 80:
            await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "specialPM", 1, formatted_now)
            if lang == 'uz':
                await message.answer(bazaga_qoshildi_uz_pm(subject,test_id, user_answers))
                await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                await Main.main_menu.set()
            elif lang == 'en':
                await message.answer(bazaga_qoshildi_en_pm(subject,test_id, user_answers))
                await message.answer("🏡 Main menu", reply_markup=en_main())
                await Main.main_menu.set()


        else:
            if lang == 'uz':
                await message.answer(uz_link_pm, reply_markup=ReplyKeyboardRemove())
                await message.answer('Kiriting: ⬇️')
                return
            elif lang == 'en':
                await message.answer(en_link_pm, reply_markup=ReplyKeyboardRemove())
                await message.answer('Enter: ⬇️')
                return



@dp.message_handler(state="getABQuestions")
async def addPMQ(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    time_format = '%d.%m.%Y'
    formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
    test_id = random.randint(0, 999999)
    full_answer = message.text
    if "*" in full_answer:
        where_is_star = full_answer.find("*")
        where_is_star = int(where_is_star)
        where_is_star += 1
        answers = full_answer[where_is_star:]
        where_is_star -= 1
        subject = full_answer[:where_is_star]
        user_answers = re.sub('[^a-zA-Z]+', '', answers)
        user_answers = user_answers.lower()
        length = len(user_answers)
        if answers.isdigit():
            if lang == 'uz':
                await message.answer(uz_link_a, reply_markup=ReplyKeyboardRemove())
                await message.answer('Kiriting: ⬇️')
                return
            elif lang == 'en':
                await message.answer(en_link_a, reply_markup=ReplyKeyboardRemove())
                await message.answer('Enter: ⬇️')
                return
        #
        if len(user_answers) == 90:
            await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "specialA", 1, formatted_now)
            if lang == 'uz':
                await message.answer(bazaga_qoshildi_uz_a(subject,test_id, user_answers))
                await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                await Main.main_menu.set()
            elif lang == 'en':
                await message.answer(bazaga_qoshildi_en_a(subject,test_id, user_answers))
                await message.answer("🏡 Main menu", reply_markup=en_main())
                await Main.main_menu.set()
            

        else:
            await message.answer(en_link_pm, reply_markup=ReplyKeyboardRemove())
            await message.answer('Enter: ⬇️')
            return


