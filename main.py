from aiogram.utils import executor
from bot_support import dp
from handlers import client, stock, other_stock


client.register_handlers_client(dp)
other_stock.register_handlers_nasdaq(dp)
stock.register_handlers_ru_market(dp)

if __name__ == '__main__':
    executor.start_polling(dp)







