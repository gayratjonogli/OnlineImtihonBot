import re
from pytz import timezone
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.types.message import Message
from keyboards.default.main_menu import uz_main, en_main
from datetime import date, datetime
from loader import dp, db, bot
from aiogram.dispatcher import FSMContext
from states.main_state import Main
import random
from .texts import qoshish_yoriqnomasi_uz, qoshish_yoriqnomasi_en, bazaga_qoshildi_uz, bazaga_qoshildi_en
from data.config import ADMINS



add_text = ["➕ Test qo'shish", "➕ Add test"]
@dp.message_handler(text=add_text, state=Main.main_menu)
async def fstep(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    home_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if lang == 'uz':
        home_btn.add('🏡 Bosh menyu')
        await message.answer(qoshish_yoriqnomasi_uz(), reply_markup=home_btn)
        await state.set_state("second")

    elif lang == 'en':
        home_btn.add('🏡 Main menu')
        await message.answer(qoshish_yoriqnomasi_en(), reply_markup=home_btn)
        await state.set_state("second")

    



@dp.message_handler(state="second")
async def sstep(message: Message, state: FSMContext):
    lang = await db.getUser_lang(message.from_user.id)
    time_format = '%d.%m.%Y'
    formatted_now = datetime.now(timezone('Asia/Tashkent')).strftime(time_format)
    if lang == 'uz':
        test_id = random.randint(0, 999999)
        full_test = message.text

        if full_test == "🏡 Bosh menyu":
            await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
            await Main.main_menu.set()
        else:
            if "*" in full_test:
                where_is_star = full_test.find("*")
                where_is_star = int(where_is_star)
                where_is_star += 1

                answers = full_test[where_is_star:]
                if answers.isdigit():
                    await message.answer(qoshish_yoriqnomasi_uz(), reply_markup=ReplyKeyboardRemove())
                    return
                else:
                    pass
                # need to change so that only with command user can add PM and A
                where_is_star -= 1
                subject = full_test[:where_is_star]
                user_answers = re.sub('[^a-zA-Z]+', '', answers)
                user_answers = user_answers.lower()
                length = len(user_answers)
                await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "usual", 1, formatted_now)

                await message.answer(bazaga_qoshildi_uz(subject, test_id, user_answers))
                await message.answer("🏡 Bosh menyu", reply_markup=uz_main())
                await Main.main_menu.set()

            else:
                await message.answer(qoshish_yoriqnomasi_uz(), reply_markup=ReplyKeyboardRemove())
                await state.set_state("second")

    elif lang == 'en':
        test_id = random.randint(0, 999999)
        full_test = message.text

        if full_test == "🏡 Main menu":
            await message.answer("🏡 Main menu", reply_markup=en_main())
            await Main.main_menu.set()
        else:
            if "*" in full_test:
                where_is_star = full_test.find("*")
                where_is_star = int(where_is_star)
                where_is_star += 1

                answers = full_test[where_is_star:]
                if answers.isdigit():
                    await message.answer(qoshish_yoriqnomasi_en(), reply_markup=ReplyKeyboardRemove())
                    return
                else:
                    pass

                where_is_star -= 1
                subject = full_test[:where_is_star]
                user_answers = re.sub('[^a-zA-Z]+', '', answers)
                user_answers = user_answers.lower()
                length = len(user_answers)
                if length == 80:
                    await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "specialPM", 1, formatted_now)
                elif length == 90:
                    await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "specialA", 1, formatted_now)
                else:
                    await db.add_test(subject, test_id, user_answers, length, message.from_user.id, "usual", 1, formatted_now)
                await message.answer(bazaga_qoshildi_en(subject, test_id, user_answers))
                await message.answer("🏡 Main menu", reply_markup=en_main())
                await Main.main_menu.set()

            else:
                await message.answer(qoshish_yoriqnomasi_en(), reply_markup=ReplyKeyboardRemove())
                await state.set_state("second")


