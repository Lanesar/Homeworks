from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, Admin
from kb import cancel_markup
import bot_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.from_user.id == Admin and message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await bot.send_message(
            message.chat.id,
            f"Hello {message.from_user.full_name}, please send us the image of your dish.",
            reply_markup=cancel_markup
        )
    else:
        await message.answer("Only available for an admin in DMs!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Please enter the name of your dish:")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Enter the dish description:")


async def load_des(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer("What is the price of the dish?")


async def load_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['price'] = int(message.text)
        await bot_db.sql_command_ins(state)
        await message.answer("Thank you, that is all.")
        await state.finish()
    except:
        await message.answer("Please enter the PRICE of the dish, in numbers.")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("Cancelled successfully.")


async def delete_data(message: types.Message):
    if message.from_user.id == Admin:
        result = await bot_db.sql_command_all()
        for i in result:
            await bot.send_photo(message.from_user.id,
                                 i[0],
                                 caption=f"Name: {i[1]}\n"
                                         f"Description: {i[2]}\n"
                                         f"Price: {i[3]}\n",
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     f"delete {i[1]}",
                                     callback_data=f'delete {i[1]}'
                                 ))
                                 )
    else:
        await message.answer("Only available to an Admin.")


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace('delete ', ''))
    await call.answer(text=f"{call.data.replace('delete ', '')} deleted", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def reg_handler_fsmres(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands="cancel")
    dp.register_message_handler(cancel_registration,
                                Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(fsm_start, commands=['res'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_des, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_data, commands=["del"])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and
                                                    call.data.startswith("delete"))