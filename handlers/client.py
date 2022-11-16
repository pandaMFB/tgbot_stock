from aiogram import types, Dispatcher
from bot_support import dp
import keybords.client_kb as nav

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Choose one of the available categories\n\n", reply_markup=nav.mainMenu)

@dp.message_handler()
async def mMenu(message: types.Message):
    if message.text == 'Stock':
        await message.reply("Choose one of the available categories\n\n", reply_markup=nav.stockMenu)

    elif message.text == 'Main menu':
        await message.reply("Choose one of the available categories\n\n", reply_markup=nav.mainMenu)

    elif message.text == 'Currency':
        await message.reply("Choose one of the available categories\n\n", reply_markup=nav.currencyMenu)

    elif message.text == 'Index':
        await message.reply("Choose one of the available categories\n\n", reply_markup=nav.indexMenu)

    else:
        await message.reply("Oops?! what?")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])