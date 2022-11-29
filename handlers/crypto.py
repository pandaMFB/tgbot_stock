import random
from aiogram.dispatcher.filters import Text
from bot_support import dp
from aiogram import types, Dispatcher
from FSM_states_group import FSMAdmin
from aiogram.dispatcher import FSMContext
from time import sleep
import keybords.client_kb as nav
from config import api_key_crypto
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

@dp.message_handler(lambda message: message.text and 'Crypto' in  message.text, state=None)
async def crypto_currency(message: types.Message):
    await FSMAdmin.crypto.set()
    await message.reply("\U000023F3Enter the full or part name of the crypto or its index"
                        "\n\U0001F4E2For example index: BTC/ETH/USDT"
                        "\n\U0001F4E2For example name: Bitcoin/Ethereum/Tether")

@dp.message_handler(Text(equals='Exit', ignore_case=True), state="*")
@dp.message_handler(content_types=['text'], state=FSMAdmin.crypto)
async def get_crypto_currency(message: types.Message, state: FSMContext):

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': f'{api_key_crypto}'
    }

    session = Session()
    session.headers.update(headers)

    try:
        with open('files_info/cryptocurrency_info.txt', 'r') as file_c:
            for line in file_c:
                if message.text.lower() in line.lower():
                    crypto_id = line.split(':')[0]
                    crypto_name = line.split(':')[1]
                    crypto_index = line.split(':')[2]

        sleep(1)

        url_crypto = f'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?id={crypto_id}'
        response_crypto = session.get(url_crypto)
        crypto_data = json.loads(response_crypto.text)

        sleep(1)

        last_crypto_price = crypto_data['data'][f'{crypto_id}']['quote']['USD']['price']
        last_update_crypto_time = crypto_data['data'][f'{crypto_id}']['quote']['USD']['last_updated']

        await message.reply(f'\U000025FCName crypto: {crypto_name}\n'
                            f'\U000025FCIndex: {crypto_index}\n'
                            f'\U00002705Currency: USD\n'
                            f'\U00002705Last price: {last_crypto_price}\n'
                            f'\U00002705Last update time: {last_update_crypto_time}\n'
                            f'\n\n \U000021A9If you want to return to the menu press /Exit')


    except:
        if message.text != '/Exit':
            await message.reply(
                f"I don't have this crypto\U000026D4\nCheck crypto name\U00002620 \n If you want to return to the menu press /Exit \U000021A9")

        else:
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply("\U0001F6B8 Ok, You are out of the section Crypto currency", reply_markup=nav.currencyMenu)


def register_handlers_crypto(dp: Dispatcher):
    dp.register_message_handler(crypto_currency, lambda message: message.text and 'Crypto' in message.text)
    dp.register_message_handler(get_crypto_currency, content_types=['text'], state=FSMAdmin.crypto)