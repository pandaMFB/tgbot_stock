from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMAdmin(StatesGroup):
    start = State()
    other_stock = State()
    stock = State()
    currency = State()
    index = State()