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
import re
from data.config import db

'''USD REAL DEFAULT 0,
                            EUR REAL DEFAULT 0,
                            PLN REAL DEFAULT 0,
                            GBP REAL DEFAULT 0,
                            CHF REAL DEFAULT 0,
                            CNY REAL DEFAULT 0,
                            CAD REAL DEFAULT 0'''


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Доброго дня! Вас вітає компанія Партнер.')
    await asyncio.sleep(2)
    await message.answer('🔥 Виберіть місто 🔥', reply_markup=city_user)


@dp.message_handler(text='🏙 Дніпро')
async def curs_valute(message: types.Message):
    sale_carrency = [i for i in db.get_all_currency('sale').values()]
    buy_currency = [i for i in db.get_all_currency('buy').values()]
    zz = zip(['USD', 'EUR', 'PLN', 'GBP', 'CHF', 'CNY', 'CAD'], buy_currency, sale_carrency)
    result_string = ''
    result_string = ''.join([f'{i[0]}: {i[1]} - {i[2]}\n' for i in zz])
    await message.answer(result_string)
    await message.answer('🔥 Бажаєте купити чи продати валюту ? 🔥', reply_markup=buy_sale_menu)


@dp.message_handler(text='Скасувати')
async def process_cancel(message: types.Message):
    await message.answer('🔥 Виберіть місто 🔥', reply_markup=city_user)


@dp.message_handler(text='🔥 Купити 🔥')
async def number(message: types.Message):
    await storage.set_state(chat=message.chat.id, state='buy')
    await message.answer('Оберіть валюту: ', reply_markup=currency_menu)


@dp.message_handler(state='buy')
async def moneta(message: types.Message, state: FSMContext):
    result = (emoji_pattern.sub(r'', message.text).strip())
    print(result)
    if result.lower() == "скасувати":
        await message.answer('🔥 Виберіть місто 🔥', reply_markup=city_user)
        await state.finish()
        return
    buy_coin = db.get_all_currency_dict('buy').get(result)
    print(buy_coin, type(buy_coin))
    if buy_coin is None:
        # await message.answer('Введите правильную валюту')
        return
    await message.answer(f'Курс: {buy_coin}')
    await state.update_data(data={'valuta_buy': result})
    await state.set_state(state='summa_buy')
    await message.answer('❓ Напишіть суму, яку треба купити/продати:', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='summa_buy')
async def number(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        return
    await state.update_data(data={'adress_buy': amount})
    balance = await state.get_data()
    print(balance)
    await message.answer(f'Cумма: {balance["adress_buy"]}')
    await state.set_state(state='adress')
    await message.answer('Оберіть відділення:', reply_markup=adress_otdel)


@dp.message_handler(state='adress')
async def number(message: types.Message, state: FSMContext):
    await state.update_data(data={'otdel_buy': message.text})
    await state.set_state(state='number_phone')
    await message.answer('❓ Введіть свій номер телефону для підтвердження заявки:',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='number_phone')
async def end(message: types.Message, state: FSMContext):
    await state.update_data(data={'data': message.text})
    await state.set_state(state='data_buy')
    number = await state.get_data()
    await message.answer(f'Телефон: {number["data"]}')
    await message.answer('Ваша заявка відправлена до відділення!',
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Нова заявка')))
    await message.answer('https://maps.app.goo.gl/m45MNuZM5Zu3u14UA')
    await message.answer(f'Вы получите : {db.get_all_currency_dict("buy")[number["valuta_buy"]] * number["adress_buy"]}')
    data = await state.get_data()
    await bot.send_message(chat_id=id_channel, text="Надійшла заявка на купівлю\n"
                                                    f"Валюта: {data['valuta_buy']}\n"
                                                    f"Сума купівлі: {data['adress_buy']}\n"
                                                    f"Відділення: {data['otdel_buy']}\n"
                                                    f"Номер клієнта: {data['data']}")
    print(data)
    await state.finish()


@dp.message_handler(text='Скасувати')
async def cancel(message: types.Message):
    await message.answer('🔥 Бажаєте купити чи продати валюту ? 🔥', reply_markup=buy_sale_menu)


'''Продажа'''


@dp.message_handler(text='🔥 Продати 🔥')
async def number(message: types.Message):
    await storage.set_state(chat=message.chat.id, state='sale')
    await message.answer('Оберіть валюту: ', reply_markup=currency_menu)


@dp.message_handler(state='sale')
async def moneta(message: types.Message, state: FSMContext):
    result = (emoji_pattern.sub(r'', message.text).strip())
    print(result)
    if result.lower() == "скасувати":
        await message.answer('🔥 Виберіть місто 🔥', reply_markup=city_user)
        await state.finish()
        return
    coin_ = db.get_all_currency_dict('sale').get(result)
    print(result)
    if coin_ is None:
        return
    await message.answer(f'Курс: {coin_}')
    await state.update_data(data={'valuta_sale': result})
    await state.set_state(state='summa_sale')
    await message.answer('❓ Напишіть суму, яку треба купити/продати:', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='summa_sale')
async def number(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        return
    await state.update_data(data={'adress_sale': amount})
    balance_sale = await state.get_data()
    print(balance_sale)
    await message.answer(f'Cумма: {balance_sale["adress_sale"]}')
    await state.set_state(state='adress_sale')
    await message.answer('Оберіть відділення:', reply_markup=adress_otdel)


@dp.message_handler(state='adress_sale')
async def number(message: types.Message, state: FSMContext):
    await state.update_data(data={'otdel_sale': message.text})
    await state.set_state(state='number_phone_sale')
    await message.answer('❓ Введіть свій номер телефону для підтвердження заявки:',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='number_phone_sale')
async def end(message: types.Message, state: FSMContext):
    await state.update_data(data={'data_sale': message.text})
    await state.set_state(state='data_sale')
    number_sale = await state.get_data()
    await message.answer(f'Телефон: {number_sale["data_sale"]}')
    await message.answer('Ваша заявка відправлена до відділення!',
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Нова заявка')))
    await message.answer('https://maps.app.goo.gl/m45MNuZM5Zu3u14UA')
    await message.answer(f'Вы получите : {db.get_all_currency_dict("sale")[number_sale["valuta_sale"]] * number_sale["adress_sale"]}')
    data = await state.get_data()
    await bot.send_message(chat_id=id_channel, text="Надійшла заявка на продаж\n"
                                                    f"Валюта: {data['valuta_sale']}\n"
                                                    f"Сума продажу: {data['adress_sale']}\n"
                                                    f"Відділення: {data['otdel_sale']}\n"
                                                    f"Номер клієнта: {data['data_sale']}")
    print(data)
    await state.finish()


@dp.message_handler(text='Нова заявка')
async def new_order(message: types.Message):
    await message.answer('Доброго дня! Вас вітає компанія Партнер.',
                         reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await message.answer('🔥 Виберіть місто 🔥', reply_markup=city_user)


@dp.message_handler(text='Скасувати')
async def cancel(message: types.Message):
    await message.answer('🔥 Бажаєте купити чи продати валюту ? 🔥', reply_markup=buy_sale_menu)


