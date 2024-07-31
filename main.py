import asyncio
from aiogram import Bot, Dispatcher, types

from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




API_TOKEN = '7207885236:AAEAgGT7J3AP3xkf0H5IJx_LpiByNwH_cxk'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# создаем кнопки
keyboard_markup = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text='Кнопка 1', callback_data='button1'),
            types.InlineKeyboardButton(text='Кнопка 2', callback_data='button2')
        ]
    ]
)
#
# keyboard_markup = types.InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             types.InlineKeyboardButton(text='Кнопка 1', callback_data='button1'),
#             types.InlineKeyboardButton(text='Кнопка 2', callback_data='button2')
#         ],
#         [
#             types.InlineKeyboardButton(text='Кнопка 3', callback_data='button3'),
#             types.InlineKeyboardButton(text='Кнопка 4', callback_data='button4')
#         ]
#     ]
# )


commands = {
    '/start': lambda message: message.answer("Добро пожаловать в наш бот!", reply_markup=keyboard_markup),
    '/help': lambda message: message.answer("Доступные команды: /start, /help, /echo, /photo"),
    #'/echo': lambda message: message.answer(message.text),  # команда просто не нужна
    '/photo': lambda message: message.answer("Это информация о боте."),
}


@dp.message()
async def cmd_handler(message: types.Message):  # Обработчик команд
    if message.text in commands:  # обрабатываем из словаря
        await commands[message.text](message)
    elif message.text.startswith('/echo '):  # отдельно для echo
        text = message.text.replace('/echo ', '')  # заменяем echo на пустое
        await message.answer(text)



@dp.callback_query(
    lambda call: call.data in ['button1', 'button2'])  # Обработчик нажатий на кнопки
async def button_callback(call: types.CallbackQuery):
    if call.data == 'button1':
        await call.answer('Вы нажали кнопку 1!')  # Ответ на нажатие первой кнопки
    elif call.data == 'button2':
        await call.answer('Вы нажали кнопку 2!')  # Ответ на нажатие второй кнопки
    # elif call.data == 'button3':
    #     await call.answer('Вы нажали кнопку 3!')  # Ответ на нажатие третьей кнопки
    # elif call.data == 'button4':
    #     await call.answer('Вы нажали кнопку 4!')  # Ответ на нажатие четвертой кнопки

# def command_filter(message: types.Message):
#     return message.text in ['/start', '/help', '/info']
#
# @dp.message(command_filter)
# async def cmd_handler(message: types.Message):
#     if message.text == '/start':
#         await message.answer("Привет! Я простой бот.")
#     elif message.text == '/help':
#         await message.answer("Это справка по боту.")
#     elif message.text == '/info':
#         await message.answer("Это информация о боте.")



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())