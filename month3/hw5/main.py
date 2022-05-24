from aiogram.utils import executor
from config import dp
import logging
import asyncio
import notif


async def on_startup(_):
    asyncio.create_task(notif.scheduler())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)