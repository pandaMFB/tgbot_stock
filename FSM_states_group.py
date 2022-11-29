from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAdmin(StatesGroup):
    start = State()
    standart_currency = State()
    other_stock = State()
    stock = State()
    crypto = State()
    index = State()
    other_market = State()