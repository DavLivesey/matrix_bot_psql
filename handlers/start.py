#Модуль стартовых функций (/start и /registration)

import logging
from loader import router, bot
from aiogram.filters import Command
from keyboards.admins_keys import admin_keyboard, registration_keyboard, security_keyboard, one_plus_keuboard
from aiogram.enums import ParseMode
from keyboards.users_keys import user_keyboard
from config import ADMIN_CHAT
from aiogram.types import Message
from handlers.main import DBCommands

db = DBCommands()
logging.basicConfig(level=logging.INFO)

@router.message(Command("start"))
async def send_message(message: Message):
    user = message.from_user
    is_user = await db.check_user(user.id)
    role = None
    banned = await db.check_ban(user.id)
    if is_user and not banned:
        role = await db.check_user_role(user.id)
        if role == 'admin':
            await message.answer(text='Выберите действие', reply_markup=admin_keyboard)
        elif role == 'security':
            await message.answer(text='Выберите действие', reply_markup=security_keyboard)
        elif role == 'one_s':
            await message.answer(text='Выберите действие', reply_markup=one_plus_keuboard)
        elif role == 'user' or 'superuser':
            await message.answer(text='Выберите действие', reply_markup=user_keyboard)
        else:
            await message.answer(text='Нажмите /registration для оформления прав доступа')
    elif banned:
        await message.answer(text='Действия Вам запрещены')
    else:
        await registartion(message)

@router.message(Command("registration"))
async def registartion(message: Message):
    user = message.from_user
    data = {'firstname': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'user_id': user.id,
            }
    banned = await db.check_ban(user.id)
    if not banned:
        await message.answer(text=f'Запрос регистрации отправлен, ожидайте ответа администратора')
        await bot.send_message(chat_id=ADMIN_CHAT, text=f"{user.id}^\nПользователь {user.first_name} "\
                                f"{user.last_name} под ником @{user.username} запросил доступ к матрице, выберите действие",
                                reply_markup=registration_keyboard,
                                parse_mode=ParseMode.HTML)
    else:
        await message.answer(text='Действия Вам запрещены')


