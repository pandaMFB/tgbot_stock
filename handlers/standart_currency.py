from aiogram.dispatcher.filters import Text
from bot_support import dp
from aiogram import types, Dispatcher
from FSM_states_group import FSMAdmin
from aiogram.dispatcher import FSMContext
from time import sleep
import keybords.client_kb as nav
import json
import requests

@dp.message_handler(lambda message: message.text and 'Standart' in  message.text, state=None)
async def standart_currency(message: types.Message):
    await FSMAdmin.standart_currency.set()
    await message.reply("\U000023F3Enter the full or part name of the currency or its index"
                        "\nFor example index: USD/EUR/CNY"
                        "\nFor example name: USA dollar/EURO/Chinese Yuan")

@dp.message_handler(Text(equals='Exit', ignore_case=True), state="*")
@dp.message_handler(content_types=['text'], state=FSMAdmin.standart_currency)
async def get_standart_currency(message: types.Message, state: FSMContext):

    try:
        with open('files_info/currency_standart.txt', 'r') as file_s_c:
            for line in file_s_c:
                if message.text.lower() in line.lower():
                    currency_name = line.split(';')[0]
                    currency_index = line.split(';')[1]

        sleep(1)

        url_currency_standart = f"https://cash.rbc.ru/cash/json/converter_currency_rate/?currency_from={currency_index}&currency_to=RUR&source=cbrf&sum=1"
        response_url_currency_standart = requests.request("GET", url_currency_standart)
        currency_standart_info = json.loads(response_url_currency_standart.text)

        last_update_time = currency_standart_info['data']['date']
        last_info_currency = currency_standart_info['data']['rate1']
        last_info_revers_currency = currency_standart_info['data']['rate2']

        await message.reply(f'\U000025FCName Currency: {currency_name}\n'
                            f'\U000025FCIndex: {currency_index}'
                            f'\n \U00002705Last price in RUB: {last_info_currency}'
                            f'\n \U00002705Last price reverse: {last_info_revers_currency}'
                            f'\n \U00002705Last update time: {last_update_time}'
                            f'\n\n\U000021A9If you want to return to the menu press /Exit')

    except:
        if message.text != '/Exit':
            await message.reply(
                f"I don't have this currency \U000026D4\nCheck currency index/name\U00002620 \nIf you want to return to the menu press /Exit \U000021A9")

        else:
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply("\U0001F6B8Ok, You are out of the section standart currency", reply_markup=nav.currencyMenu)


def register_handlers_currency_standart(dp: Dispatcher):
    dp.register_message_handler(standart_currency, lambda message: message.text and 'Standart' in message.text)
    dp.register_message_handler(get_standart_currency, content_types=['text'], state=FSMAdmin.standart_currency)