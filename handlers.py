from main import bot, dp
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from funcs import main_func


@dp.message_handler(commands='start')
async def start(message: Message):
    await message.answer(text=f'Привет, {message.from_user.full_name}')


class SteamInfo(StatesGroup):
    steam_id = State()


@dp.message_handler(commands='info')
async def go_info(message: Message):
    await message.answer(text='Напиши стим айди')

    await SteamInfo.steam_id.set()


@dp.message_handler(state=SteamInfo.steam_id)
async def send_info(message: Message, state: FSMContext):
    steam_id = int(message.text)

    text = main_func(steam_id=steam_id)
    await bot.send_message(message.from_id, text=text)

    await state.finish()
