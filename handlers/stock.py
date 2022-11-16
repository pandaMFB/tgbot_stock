from aiogram.dispatcher.filters import Text
from bot_support import dp
from aiogram import types, Dispatcher
from FSM_states_group import FSMAdmin
from aiogram.dispatcher import FSMContext
import requests
import json
from time import sleep
import keybords.client_kb as nav

@dp.message_handler(lambda message: message.text and 'MOEX market' in  message.text, state=None)
async def stock_start(message: types.Message):
    await FSMAdmin.stock.set()
    await message.reply("Enter the full or part name of the stock or its index"
                        "'\n'For example index: VKCO/GAZP/YNDX")


@dp.message_handler(Text(equals='Exit', ignore_case=True), state="*")
@dp.message_handler(content_types=['text'], state=FSMAdmin.stock)
async def get_stock_infa(message: types.Message, state: FSMContext):

        try:
            list_index_by_name = []
            list_name_of_index = []

            with open('files_info/all_index_moex.txt', 'r') as file:
                for line in file:
                    if message.text.lower() in line.lower():
                        index_by_name = line.partition(':')[0]
                        name_of_index = line.partition(':')[2]

                        list_name_of_index.append(name_of_index)
                        list_index_by_name.append(index_by_name)

            if len(list_index_by_name) > 1:

                await message.reply(f'Number of records found for your query: {len(list_index_by_name)}'
                                    f'\nThe name of the shares is the same, but their index is different')

                sleep(1.5)

                for index in list_index_by_name:
                    url_get_info_index = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{index}/.json"
                    response_get_info_index = requests.request("GET", url_get_info_index)
                    get_info_index_convert = json.loads(response_get_info_index.text)

                    if len(get_info_index_convert['marketdata']['data']) != 0:

                        for item in get_info_index_convert['marketdata']['data']:
                            open_info_index = item[9]
                            low_info_index = item[10]
                            high_info_index = item[11]
                            last_info_index = item[12]

                            for name in list_name_of_index:
                                sleep(0.5)
                                await message.reply(f'Name: {name}'
                                                    f'Currency: RUB\n'
                                                    f'Index: {index}'
                                                    '\n'
                                                    f'\n Last price: {last_info_index}'
                                                    f'\n Open price: {open_info_index}'
                                                    f'\n High price today: {high_info_index}'
                                                    f'\n Low price today: {low_info_index}'
                                                    f'\n\n If you want to return to the menu press /Exit')
                                del list_name_of_index[0]
                                break
                    else:
                        sleep(0.5)
                        del list_name_of_index[0]
                        await message.reply(f"By index:{index} - no data")

            else:
                await message.reply(f'An entry was found for your request: {list_name_of_index[0]}')

                sleep(0.5)

                url_get_info_index = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{list_index_by_name[0]}/.json"
                response_get_info_index = requests.request("GET", url_get_info_index)
                get_info_index_convert = json.loads(response_get_info_index.text)

                for item in get_info_index_convert['marketdata']['data']:
                    open_info_index = item[9]
                    low_info_index = item[10]
                    high_info_index = item[11]
                    last_info_index = item[12]

                await message.reply(f'Currency: RUB\n'
                                    f'Index: {list_index_by_name[0]}'
                                    '\n'
                                    f'\n Last price: {last_info_index}'
                                    f'\n Open price: {open_info_index}'
                                    f'\n High price today: {high_info_index}'
                                    f'\n Low price today: {low_info_index}'
                                    f'\n\n If you want to return to the menu press /Exit')

        except:
            if message.text != '/Exit':
                await message.reply("I don't have this stock\n Check stock name\U00002620 \n If you want to return to the menu press /Exit")

            else:
                current_state = await state.get_state()
                if current_state is None:
                    return
                await state.finish()
                await message.reply("Ok, You are out of the section RU market stock", reply_markup=nav.stockMenu)


def register_handlers_ru_market(dp: Dispatcher):
    dp.register_message_handler(stock_start, lambda message: message.text and 'MOEX market' in  message.text)
    dp.register_message_handler(get_stock_infa, content_types=['text'], state=FSMAdmin.stock)