from config import token_bot_tg
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=token_bot_tg)
dp = Dispatcher(bot, storage=storage)