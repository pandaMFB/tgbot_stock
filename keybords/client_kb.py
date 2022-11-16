from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but_main = KeyboardButton('Main menu')

but_stock = KeyboardButton('Stock')
but_currency = KeyboardButton('Currency')
but_index = KeyboardButton('Index')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_stock, but_currency, but_index)

but_stock_ru = KeyboardButton('MOEX market')
but_stock_other = KeyboardButton('NASDAQ market')

stockMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_stock_ru, but_stock_other, but_main)

but_currency = KeyboardButton('/Standart_currency')
but_currency_crypta = KeyboardButton('/Crypto_currency')

currencyMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_currency, but_currency_crypta, but_main)

but_index_ru = KeyboardButton('/RU_index')
but_index_other = KeyboardButton('/Nasdaq_index')

indexMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(but_index_ru, but_index_other, but_main)