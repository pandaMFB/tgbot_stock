from aiogram.dispatcher.filters import Text
from bot_support import dp
from aiogram import types, Dispatcher
from FSM_states_group import FSMAdmin
from aiogram.dispatcher import FSMContext
import requests
import json
from time import sleep
import keybords.client_kb as nav
from config import api_key_alpha_1

@dp.message_handler(lambda message: message.text and 'NASDAQ market' in  message.text, state=None,)
async def other_stock_start(message: types.Message):
    await FSMAdmin.other_stock.set()
    await message.reply("Enter the full or part name of the stock or its index"
                        "'\n'For example index: AAPL/AMZN/MRNA"
                        "'\n'For example name: Apple/Amazon/Moderna")

@dp.message_handler(Text(equals='Exit', ignore_case=True), state="*")
@dp.message_handler(content_types=['text'], state=FSMAdmin.other_stock)
async def get_other_stock_infa(message: types.Message, state: FSMContext):

    try:
        list_index_nasdaq = []
        list_name_nasdaq = []
        error_message = 'Error Message'

        with open('files_info/nasdaq_index_stock_all.txt', 'r') as file:
            for line in file:
                if message.text.lower() in line.lower():
                    index_nasdaq = line.partition(';')[0]
                    name_nasdaq = line.partition(';')[2]

                    list_index_nasdaq.append(index_nasdaq)
                    list_name_nasdaq.append(name_nasdaq)
        if len(list_index_nasdaq) > 1:

            await message.reply(f'Number of records found for your query: {len(list_index_nasdaq)}'
                                f'\nThe name of the shares is the same, but their index is different')

            sleep(1.5)

            for index in list_index_nasdaq:
                url_info_index_nasdaq = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={index}&interval=5min&apikey={api_key_alpha_1}&outputsize=compact&datatype=json"
                response_info_index_nasdaq = requests.request("GET", url_info_index_nasdaq)
                json_url_info_index_nasdaq = json.loads(response_info_index_nasdaq.text)

                if error_message in json_url_info_index_nasdaq:
                    await message.reply(f"By index:{index} - no data")
                else:
                    last_time_update = json_url_info_index_nasdaq['Meta Data']['3. Last Refreshed']
                    last_price_stock = json_url_info_index_nasdaq['Time Series (5min)'][f'{last_time_update}']['4. close']
                    last_volume_stock = json_url_info_index_nasdaq['Time Series (5min)'][f'{last_time_update}']['5. volume']

                    for name in list_name_nasdaq:
                        sleep(0.5)
                        await message.reply(f'Name: {name}'
                                            f'Currency: USD\n'
                                            f'Index: {index}'
                                            '\n'
                                            f'\n Last price: {last_price_stock}'
                                            f'\n Last time update: {last_time_update}'
                                            f'\n Volume at last update: {last_volume_stock}'
                                            f'\n\n If you want to return to the menu press /Exit')
                        del list_name_nasdaq[0]
                        break
        else:
            await message.reply(f'An entry was found for your request: {list_index_nasdaq[0]}')

            sleep(1.5)

            for index in list_index_nasdaq:
                url_info_index_nasdaq = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={index}&interval=5min&apikey={api_key_alpha_1}&outputsize=compact&datatype=json"
                response_info_index_nasdaq = requests.request("GET", url_info_index_nasdaq)
                json_url_info_index_nasdaq = json.loads(response_info_index_nasdaq.text)

                if error_message in json_url_info_index_nasdaq:
                    await message.reply(f"By index:{index} - no data")
                else:
                    last_time_update = json_url_info_index_nasdaq['Meta Data']['3. Last Refreshed']
                    last_price_stock = json_url_info_index_nasdaq['Time Series (5min)'][f'{last_time_update}']['4. close']
                    last_volume_stock = json_url_info_index_nasdaq['Time Series (5min)'][f'{last_time_update}']['5. volume']

                    for name in list_name_nasdaq:
                        sleep(0.5)
                        await message.reply(f'Name: {name}'
                                            f'Currency: USD\n'
                                            f'Index: {index}'
                                            '\n'
                                            f'\n Last price: {last_price_stock}'
                                            f'\n Last time update: {last_time_update}'
                                            f'\n Volume at last update: {last_volume_stock}'
                                            f'\n\n If you want to return to the menu press /Exit')

    except:
        if message.text != '/Exit':
            await message.reply(
                "I don't have this stock\n Check stock name\U00002620 \n If you want to return to the menu press /Exit")

        else:
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply("Ok, You are out of the section Other market stock", reply_markup=nav.stockMenu)

def register_handlers_nasdaq(dp: Dispatcher):
    dp.register_message_handler(other_stock_start, lambda message: message.text and 'NASDAQ market' in  message.text)
    dp.register_message_handler(get_other_stock_infa, content_types=['text'], state=FSMAdmin.other_stock)