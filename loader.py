import asyncio
import logging
from config import BOT_TOKEN
from sql import create_pool
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Router, Dispatcher

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s'
                           u'[%(asctime)s]  %(message)s',
                    level=logging.INFO)
loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())
bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
router = Router()
dp = Dispatcher()