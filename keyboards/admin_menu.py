from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_buy = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Зміни Покупки'),
                                                          KeyboardButton(text='Зміни Продажу'))


admin_currency_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('🇺🇸 USD 🇺🇸'),
                                                      KeyboardButton(text='🇩🇪 EUR 🇩🇪'),
                                                      KeyboardButton(text='🇵🇱 PLN 🇵🇱'),
                                                      KeyboardButton(text='🇬🇧 GBP 🇬🇧'),
                                                      KeyboardButton(text='🇨🇭 CHF 🇨🇭'),
                                                      KeyboardButton(text='🇨🇳 CNY 🇨🇳'),
                                                      KeyboardButton(text='🇨🇦 CAD 🇨🇦'),
                                                      KeyboardButton(text='Скасувати'))

main_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Головне меню'))
