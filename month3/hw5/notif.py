import asyncio
import aioschedule
from config import bot


async def internet_notif():
    await bot.send_message(chat_id=5296495923, text="Your packet resets today.")


async def scheduler():
    aioschedule.every().tuesday.at("12:00").do(internet_notif)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(59)


