import logging
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Router, Dispatcher

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s'
                           u'[%(asctime)s]  %(message)s',
                    level=logging.INFO)

bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
router = Router()
dp = Dispatcher()

