from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


city_user = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='🏙 Дніпро'))
buy_sale_menu = ReplyKeyboardMarkup(resize_keyboard=True, ).add(KeyboardButton(text='🔥 Купити 🔥'),
                                                      KeyboardButton(text='🔥 Продати 🔥'),
                                                      KeyboardButton('Скасувати'))


currency_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('🇺🇸 USD 🇺🇸'),
                                                      KeyboardButton(text='🇩🇪 EUR 🇩🇪'),
                                                      KeyboardButton(text='🇵🇱 PLN 🇵🇱'),
                                                      KeyboardButton(text='🇬🇧 GBP 🇬🇧'),
                                                      KeyboardButton(text='🇨🇭 CHF 🇨🇭'),
                                                      KeyboardButton(text='🇨🇳 CNY 🇨🇳'),
                                                      KeyboardButton(text='🇨🇦 CAD 🇨🇦'),
                                                      KeyboardButton(text='Скасувати'))

#new_order = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Нова заявка'))


adress_otdel = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Вулиця Челюскіна, 8А, Дніпро'))

