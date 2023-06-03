from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Restart"),
            types.BotCommand('prezident_school', "Test yaratish/Create test"),
            types.BotCommand('abiturient', "Test yaratish/Create test"),
            types.BotCommand("help", "Yordam"),
        ]
    )
