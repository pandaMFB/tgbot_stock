from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but_main = KeyboardButton('Main menu')

but_stock = KeyboardButton('Stock')
but_currency = KeyboardButton('Currency')
but_index = KeyboardButton('Index')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_stock, but_currency, but_index)

but_stock_ru = KeyboardButton('MOEX')
but_stock_other = KeyboardButton('NASDAQ')

stockMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_stock_ru, but_stock_other, but_main)

but_currency_standart = KeyboardButton('Standart')
but_currency_crypto = KeyboardButton('Crypto')

currencyMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_currency_standart, but_currency_crypto, but_main)

but_index_ru = KeyboardButton('All list')
but_index_other = KeyboardButton('Other')

indexMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_index_ru, but_index_other, but_main)