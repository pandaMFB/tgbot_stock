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

@dp.message_handler(lambda message: message.text and 'NASDAQ' in  message.text, state=None,)
async def other_stock_start(message: types.Message):
    await FSMAdmin.other_stock.set()
    await message.reply("\U000023F3Enter the full or part name of the stock or its index"
                        "\nFor example index: AAPL/AMZN/MRNA"
                        "\nFor example name: Apple/Amazon/Moderna")

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

            await message.reply(f'\U00002757 Number of records found for your query: {len(list_index_nasdaq)}'
                                f'\nThe name of the shares is the same, but their index is different')

            sleep(1.5)

            for index in list_index_nasdaq:
                url_info_index_nasdaq = f'https://api.bcs.ru/udfdatafeed/v1/info?inOrderArray=true&instruments=SPBXM|{index}'
                response_info_index_nasdaq = requests.request("GET", url_info_index_nasdaq)
                json_url_info_index_nasdaq = json.loads(response_info_index_nasdaq.text)

                if error_message in json_url_info_index_nasdaq:
                    await message.reply(f"\U0000274CBy index:{index} - no data")
                else:
                    for elem in json_url_info_index_nasdaq:
                        last_time_update = elem['info']['lastTradeDate']
                        last_price_stock = elem['info']['close']
                        last_volume_stock = elem['info']['value']
                        currencyCode = elem['currencyCode']
                        kotirovki_company = f"https://bcs-express.ru{elem['relativeReference']}"

                for name in list_name_nasdaq:
                        sleep(0.5)
                        await message.reply(f'\U000025FCName: {name}\n'                                           
                                            f'\U000025FCCurrency: {currencyCode}\n'
                                            f'\U000025FCIndex: {index}\n'
                                            f'\n \U00002705Last price: {last_price_stock}'                                           
                                            f'\n \U00002705Volume at last update: {last_volume_stock}'
                                            f'\n \U00002705Last time update:\n{last_time_update}'
                                            f'\n \U00002705Diagram:\n{kotirovki_company}\n'
                                            f'\n\n \U000021A9If you want to return to the menu press /Exit')
                        del list_name_nasdaq[0]
                        break
        else:
            await message.reply(f'\U000023F3An entry was found for your request: {list_index_nasdaq[0]}')

            sleep(1.5)

            for index in list_index_nasdaq:
                url_info_index_nasdaq = f'https://api.bcs.ru/udfdatafeed/v1/info?inOrderArray=true&instruments=SPBXM|{index}'
                response_info_index_nasdaq = requests.request("GET", url_info_index_nasdaq)
                json_url_info_index_nasdaq = json.loads(response_info_index_nasdaq.text)

                if error_message in json_url_info_index_nasdaq:
                    await message.reply(f"\U0000274CBy index:{index} - no data")
                else:
                    for elem in json_url_info_index_nasdaq:
                        last_time_update = elem['info']['lastTradeDate']
                        last_price_stock = elem['info']['close']
                        last_volume_stock = elem['info']['value']
                        currencyCode = elem['currencyCode']
                        kotirovki_company = f"https://bcs-express.ru{elem['relativeReference']}"

                    for name in list_name_nasdaq:
                        sleep(0.5)
                        await message.reply(f'\U000025FCName: {name}'                                           
                                            f'\U000025FCCurrency: {currencyCode}\n'
                                            f'\U000025FCIndex: {index}\n'
                                            f'\n \U00002705Last price: {last_price_stock}'                                           
                                            f'\n \U00002705Volume at last update: {last_volume_stock}'
                                            f'\n \U00002705Last time update:\n{last_time_update}'
                                            f'\n \U00002705Diagram:\n{kotirovki_company}\n'
                                            f'\n\n \U000021A9If you want to return to the menu press /Exit')

    except:
        if message.text != '/Exit':
            await message.reply(
                "I don't have this stock\U000026D4\n Check stock name\U00002620 \n If you want to return to the menu press /Exit \U000021A9")

        else:
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply("\U0001F6B8Ok, You are out of the section Other market stock", reply_markup=nav.stockMenu)

def register_handlers_nasdaq(dp: Dispatcher):
    dp.register_message_handler(other_stock_start, lambda message: message.text and 'NASDAQ' in  message.text)
    dp.register_message_handler(get_other_stock_infa, content_types=['text'], state=FSMAdmin.other_stock)