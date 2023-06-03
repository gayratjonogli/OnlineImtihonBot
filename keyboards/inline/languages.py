from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def language_btn():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.insert(InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='til:uz'))
    btn.insert(InlineKeyboardButton(text="🇬🇧 English", callback_data='til:en'))
    return btn