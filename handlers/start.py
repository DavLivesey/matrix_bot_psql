#from .callbacks.admins import ADDUSER
import logging
from loader import bot, router, dp
from aiogram.filters import Command
from aiogram.enums import ParseMode
from keyboards.admins_keys import admin_keyboard
from keyboards.users_keys import user_keyboard
from config import ADMIN_LIST, ADMIN_CHAT
from aiogram.types import Message



logging.basicConfig(level=logging.INFO)

@router.message(Command("start"))
async def send_message(message: Message):
    user = message.from_user
    user_id = user.id
    await bot.send_message(chat_id=ADMIN_CHAT, text=f"Пользователь {user.first_name} "\
                            f"{user.last_name} под ником @{user.username} запустил матрицу",
                              parse_mode=ParseMode.HTML)


    if user_id in ADMIN_LIST:
        await message.answer(text='Что Вы хотите делать?', reply_markup=admin_keyboard)
    else:
        await message.answer(text='Что Вы хотите делать?', reply_markup=user_keyboard) 


