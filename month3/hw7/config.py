from decouple import config
from aiogram import Bot, Dispatcher


Token = config("TOKEN")

bot = Bot(Token)
dp = Dispatcher(bot=bot)

ADMIN = 5296495923