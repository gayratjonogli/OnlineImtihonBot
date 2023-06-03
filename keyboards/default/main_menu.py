from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def uz_main():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Test qo'shish"),
                KeyboardButton(text="🔑 Test tekshirish")
            ],
            [
                KeyboardButton(text="📊 Reyting ko'rish")
            ],
            [
                KeyboardButton(text="📑 Mening testlarim")
            ],
            [
                KeyboardButton(text="📁 Mening ma'lumotlarim"),
                KeyboardButton(text="⚙️ Sozlamalar")
            ]
    ],
    resize_keyboard=True, one_time_keyboard=True
    )
    return markup



def en_main():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Add test"),
                KeyboardButton(text="🔑 Check test")
            ],
            [
                KeyboardButton(text="📊 Ratings")
            ],
            [
                KeyboardButton(text="📑 My tests")
            ],
            [
                KeyboardButton(text="📁 My information"),
                KeyboardButton(text="⚙️ Settings")
            ]
    ],
    resize_keyboard=True, one_time_keyboard=True
    )
    return markup


def change_name_uz():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔀 Ismni o'zgartirish"),
            ],
            [
                KeyboardButton(text="🏡 Bosh menyu")
            ]
    ],
    resize_keyboard=True, one_time_keyboard=True
    )
    return markup


def change_name_en():
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔀 Change name"),
            ],
                        [
                KeyboardButton(text="🏡 Main menu")
            ]
    ],
    resize_keyboard=True, one_time_keyboard=True
    )
    return markup