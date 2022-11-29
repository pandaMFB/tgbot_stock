import requests
from aiogram.dispatcher.filters import Text
from bot_support import dp
from aiogram import types, Dispatcher
from FSM_states_group import FSMAdmin
from aiogram.dispatcher import FSMContext
from time import sleep
import keybords.client_kb as nav
import json

@dp.message_handler(lambda message: message.text and 'All list' in  message.text, state=None)
async def index_info(message: types.Message):
    await FSMAdmin.index.set()
    await message.reply("\U000023F3List of available Indices:"
                        "\nNAME : INDEX"
                        "\nINDEX MOSBIRZHA:IMOEX"
                        "\nINDEX RTS:RTSI"
                        "\nINDEX NASDAQ:NSDComposite"
                        "\nINDEX S&P500:S&P500"
                        "\n\n\n\U0001F4E2Enter an available index or name/part name")


@dp.message_handler(Text(equals='Exit', ignore_case=True), state="*")
@dp.message_handler(content_types=['text'], state=FSMAdmin.index)
async def get_info_index(message: types.Message, state: FSMContext):
    try:
        with open('files_info/all_index.txt', 'r') as file:
            for line in file:
                if message.text.lower() in line.lower():
                    index_id = line.split(';')[0]
                    index_name = line.split(';')[1]
                    index_url = line.split(';')[2]

                    sleep(1)

                    response_index = requests.request("GET", index_url)
                    Index_json = json.loads(response_index.text)

        sleep(1)

        for elem in Index_json:
            last_time_update = elem['info']['lastTradeDate']
            last_price_index = elem['info']['close']
            last_price_open_index = elem['info']['open']
            last_volume_index = elem['info']['value']
            kotirovki_index = f"https://bcs-express.ru{elem['relativeReference']}"

            await message.reply(f'\U000025FCName: {index_name}'
                                f'\n \U00002705Last price: {last_price_index}'
                                f'\n \U00002705Open price: {last_price_open_index}'
                                f'\n \U00002705Volume at last update: {last_volume_index}'
                                f'\n \U00002705Last time update:\n{last_time_update}'
                                f'\n \U00002705Diagram:\n{kotirovki_index}\n'
                                f'\n\n \U000021A9If you want to return to the menu press /Exit')

    except:
        if message.text != '/Exit':
            await message.reply(
                "I don't have this Index\U000026D4\n Check Index name\U00002620 \n If you want to return to the menu press /Exit \U000021A9")

        else:
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply("\U0001F6B8Ok, You are out of the section all Index",
                                reply_markup=nav.indexMenu)


def register_handlers_index(dp: Dispatcher):
    dp.register_message_handler(index_info, lambda message: message.text and 'All list' in message.text)
    dp.register_message_handler(get_info_index, Text(equals='Exit', ignore_case=True), state="*")
    dp.register_message_handler(get_info_index, content_types=['text'], state=FSMAdmin.index)


