from aiogram import types, Dispatcher
from config import bot, dp
import newsp


async def parser_news(message: types.Message):
    data = newsp.parser()
    for item in data:
        await bot.send_message(message.chat.id,
                               f"{item['title']}\n"
                               f"{item['desc']}\n\n"
                               f"{item['link']}")


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(parser_news, commands=['movies'])

