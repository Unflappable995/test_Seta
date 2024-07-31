import asyncio
import sys

import logging
from aiogram import Bot, Dispatcher, types, Router

from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove




API_TOKEN = '7207885236:AAEAgGT7J3AP3xkf0H5IJx_LpiByNwH_cxk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
form_router = Router()
dp.include_router(form_router)

# создаем кнопки
keyboard_markup = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text='Кнопка 1', callback_data='button1'),
            types.InlineKeyboardButton(text='Кнопка 2', callback_data='button2')
        ]
    ]
)

commands = {
    '/start': lambda message: message.answer("Добро пожаловать в наш бот!", reply_markup=keyboard_markup),
    '/help': lambda message: message.answer("Доступные команды: /start, /help, /echo, /photo"),
    '/data': lambda message: message.answer(),  # команда просто не нужна
    '/photo': lambda message: message.answer("Это информация о боте."),
}

class Form(StatesGroup):
    name = State()
    age = State()

@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer("Добро пожаловать в наш бот!", reply_markup=keyboard_markup)
    await state.set_state(Form.name)
    await message.answer("Привет! Как тебя зовут?")


@form_router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)  # Сохраняем имя
    await state.set_state(Form.age)  # Переход к следующему состоянию
    await message.answer(f"Отлично, {message.text}! Сколько тебе лет?")


@form_router.message(Form.age)
async def process_age(message: types.Message, state: FSMContext) -> None:
    user_data = await state.get_data()  # Получаем сохраненные данные
    name = user_data.get('name')

    await message.answer(f"Ты сказал, что тебе {message.text} лет. Приятно познакомиться, {name}!")
    await state.clear()

@form_router.message()
async def cmd_handler(message: types.Message):  # Обработчик команд
    if message.text in commands:  # Обрабатываем команды из словаря
        await commands[message.text](message)
    elif message.text.startswith('/echo '):  # отдельно для echo
        text = message.text.replace('/echo ', '')  # заменяем echo на пустое
        await message.answer(text)
    else:
        await message.answer("Команда не распознана. Используйте /help для списка доступных команд.")



@dp.callback_query(
    lambda call: call.data in ['button1', 'button2'])  # Обработчик нажатий на кнопки
async def button_callback(call: types.CallbackQuery):
    if call.data == 'button1':
        await call.answer('Вы нажали кнопку 1!')  # Ответ на нажатие первой кнопки
    elif call.data == 'button2':
        await call.answer('Вы нажали кнопку 2!')  # Ответ на нажатие второй кнопки




async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())