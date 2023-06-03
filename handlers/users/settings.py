from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from loader import bot, dp, db
from states.main_state import Main
from keyboards.default.main_menu import uz_main, en_main
from keyboards.inline.languages import language_btn
from .texts import language


settings_text = ['⚙️ Settings', '⚙️ Sozlamalar']

@dp.message_handler(text=settings_text, state=Main.main_menu)
async def open_settings(message: Message, state: FSMContext):
    await message.answer(language(), reply_markup=language_btn())
    await state.set_state("gettil")


@dp.callback_query_handler(text_contains='til', state="gettil")
async def setLang(call: CallbackQuery, state: FSMContext):
    lang = call.data.rsplit(':')
    til = lang[1]
    await call.message.delete()
    await db.update_user_language(call.from_user.id, til)
    if til == 'uz':
        await call.message.answer("🏡 Bosh menyu", reply_markup=uz_main())
        await Main.main_menu.set()
    elif til == 'en':
        await call.message.answer("🏡 Main menu", reply_markup=en_main())
        await Main.main_menu.set()