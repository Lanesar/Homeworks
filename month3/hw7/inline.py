from aiogram import types, Dispatcher
import hashlib


async def inline_google_handler(query: types.InlineQuery):
    text = query.query or "echo"
    links = f"https://www.google.com/search?q={text}"
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    articles = [
        types.InlineQueryResultArticle(
            id=result_id,
            title="Google: ",
            url=links,
            input_message_content=types.InputMessageContent(
                message_text=links
            )
        )
    ]

    await query.answer(articles, cache_time=60, is_personal=True)


def register_handler_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_google_handler)