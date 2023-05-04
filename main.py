from aiogram import executor, Dispatcher
from heandlers import *
import asyncio
from data.loader import *
from services.api_sqlite import *
from data.config import *


if __name__ == '__main__':
    executor.start_polling(dp)
