import asyncio
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from data.loader import *
from aiogram import types
from os import path
from data.config import *
from keyboards import *
from aiogram.dispatcher import FSMContext
from services.api_sqlite import *
import asyncio
from keyboards.user_menu import *
from services.api_sqlite import *
from keyboards.admin_menu import *
import re
from data.config import db, user_id

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


@dp.message_handler(commands='admin')
async def admin(message: types.Message):
    if message.from_user.id in user_id:
        await message.answer('Виберіть дії, зміни продажу або зміни покупки', reply_markup=admin_buy)
    else:
        await message.answer('У вас отсутствует право админа')
'''Зміни Покупки'''


@dp.message_handler(text='Зміни Покупки')
async def change_buy(message: types.Message):
    if message.from_user.id in user_id:
        await message.answer('Виберіть валюту', reply_markup=admin_currency_menu)
        await storage.set_state(chat=message.chat.id, state='currency_buys_change')
    else:
        await message.answer('У вас отсутствует право админа')


@dp.message_handler(state='currency_buys_change')
async def process_currency_buy_change(message: types.Message, state: FSMContext):
    result = (emoji_pattern.sub(r'', message.text).strip())
    print(result)
    _currency = db.get_all_currency_dict('buy').get(result)
    print(_currency)
    if _currency is None:
        await message.answer('Введіть правильну валюту')
        return
    await message.answer(f'Текущий Курс: {_currency}')
    await state.update_data(data={'valuta_buy': result})
    await state.set_state(state='admin_buy')
    await message.answer('Введіть новий курс або натисніть кнопку Відмінити',
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Відмінити')))


@dp.message_handler(state='admin_buy')
async def process_admin_buy(message: types.Message, state: FSMContext):
    if message.text.lower() == 'відмінити':
        await message.answer('Виберіть дії, зміни продажу або зміни покупки', reply_markup=admin_buy)
        await state.finish()
    datas = await state.get_data()
    try:
        amount = float(message.text) # проверка что юзер ввел число
    except ValueError:
        await message.answer('Введіть число')
        return
    db.update_currency(datas['valuta_buy'], 'buy', amount)
    await message.answer('Валюта успішно оновлена', reply_markup=main_menu_admin)
    await state.finish()



'''Зміни Продажу'''

@dp.message_handler(text='Зміни Продажу')
async def change_buy(message: types.Message):
    if message.from_user.id in user_id:
        await message.answer('Виберіть валюту', reply_markup=admin_currency_menu)
        await storage.set_state(chat=message.chat.id, state='currency_sales_change')
    else:
        await message.answer('У вас отсутствует право админа')

@dp.message_handler(state='currency_sales_change')
async def process_currency_buy_change(message: types.Message, state: FSMContext):
    result = (emoji_pattern.sub(r'', message.text).strip())
    print(result)
    _currency = db.get_all_currency_dict('sale').get(result)
    print(_currency)
    if _currency is None:
        await message.answer('Введіть правильну валюту')
        return
    await message.answer(f'Текущий Курс: {_currency}')
    await state.update_data(data={'valuta_sale': result})
    await state.set_state(state='admin_sale')
    await message.answer('Введіть новий курс або натисніть кнопку Відмінити',
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Відмінити')))


@dp.message_handler(state='admin_sale')
async def process_admin_buy(message: types.Message, state: FSMContext):
    if message.text.lower() == 'відмінити':
        await message.answer('Виберіть дії, зміни продажу або зміни покупки', reply_markup=admin_buy)
        await state.finish()
    datas = await state.get_data()
    try:
        amount = float(message.text) # проверка что юзер ввел число
    except ValueError:
        await message.answer('Введіть число')
        return
    db.update_currency(datas['valuta_sale'], 'sale', amount)
    await message.answer('Валюта успішно оновлена', reply_markup=main_menu_admin)
    await state.finish()


@dp.message_handler(text='Головне меню')
async def main_menu_admin_currency(message: types.Message):
    await message.answer('Виберіть дії, зміни продажу або зміни покупки', reply_markup=admin_buy)
