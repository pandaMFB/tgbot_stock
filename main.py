from aiogram.utils import executor
from bot_support import dp
from handlers import client, stock, other_stock, crypto, standart_currency, index, other_market

client.register_handlers_client(dp)
other_market.register_handlers_other_market(dp)
index.register_handlers_index(dp)
standart_currency.register_handlers_currency_standart(dp)
crypto.register_handlers_crypto(dp)
other_stock.register_handlers_nasdaq(dp)
stock.register_handlers_ru_market(dp)

if __name__ == '__main__':
    executor.start_polling(dp)







