from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import config_file


storage = MemoryStorage()
bot = Bot(token=config_file['token'])
dp = Dispatcher(bot, storage=storage)