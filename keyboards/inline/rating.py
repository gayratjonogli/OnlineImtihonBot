from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def rating_button_uz():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="🔀 Ulashish", switch_inline_query='aaa'))
    return markup

def rating_button_en():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="🔀 Share", switch_inline_query='aaa'))
    return markup


def end_test_uz(test_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="📊 Reyting", callback_data=f"creator:rating:{test_id}"))
    markup.insert(InlineKeyboardButton(text="🔴 Yakunlash", callback_data=f"creator:end_test:{test_id}"))
    return markup


def end_test_en(test_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="📊 Rating", callback_data=f"creator:rating:{test_id}"))
    markup.insert(InlineKeyboardButton(text="🔴 End test", callback_data=f"creator:end_test:{test_id}"))
    return markup


def see_errors_uz(user_id, test_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="👁 Xatolarni ko'rish", callback_data=f"error:{user_id}:{test_id}"))
    return markup


def see_errors_en(user_id, test_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="👁 View errors", callback_data=f"error:{user_id}:{test_id}"))
    return markup



def reyting_uz(test_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="📊 Reyting", callback_data=f"rating:{test_id}"))
    return markup


def reyting_en(test_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="📊 Rating", callback_data=f"rating:{test_id}"))
    return markup