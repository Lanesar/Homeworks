from aiogram.utils import executor
from config import dp
import fsm
import logging
import bot_db



async def on_startup(_):
    bot_db.sql_create()


fsm.reg_handler_fsmres(dp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)