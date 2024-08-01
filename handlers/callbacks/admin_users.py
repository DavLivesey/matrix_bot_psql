#Модуль раздачи прав пользователям

from aiogram import types, F, Router
from .admins import database
from keyboards.admins_keys import AdminCallback
from loader import bot

admins_router = Router(name=__name__)

@admins_router.callback_query(AdminCallback.filter(F.text == 'admin'))
async def add_admin_user(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    existing = await database.check_user(data.id)
    if not existing:
        await database.add_user(data.first_name, data.last_name, data.username, data.id, role='admin')
        await call.message.answer(text=f'Пользователю {data.first_name} {data.last_name} предоставлены права администратора')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'Ваша регистрация успешно пройдена, теперь Вы - администратор матрицы, '\
                               f'нажмите /start для начала работы')
    else:
        await database.edit_user_role(data.id, 'admin')
        await call.message.answer(text=f'Права пользователя {data.first_name} {data.last_name} изменены на админские')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'доступ изменён, теперь Вы - администратор матрицы, '\
                               f'нажмите /start для начала работы')

@admins_router.callback_query(AdminCallback.filter(F.text == 'security'))
async def add_security_user(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    existing = await database.check_user(data.id)
    if not existing:
        await database.add_user(data.first_name, data.last_name, data.username, data.id, role='security')
        await call.message.answer(text=f'Пользователю {data.first_name} {data.last_name} предоставлены права информационной безопасности')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'Ваша регистрация успешно пройдена, теперь Вы  можете изменять даныне информационной безопасности, '\
                               f'нажмите /start для начала работы')
    else:
        await database.edit_user_role(data.id, 'security')
        await call.message.answer(text=f'Права пользователя {data.first_name} {data.last_name} изменены на информационную безопасность')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'доступ изменён, теперь Вы  можете изменять даныне информационной безопасности, '\
                               f'нажмите /start для начала работы')

@admins_router.callback_query(AdminCallback.filter(F.text == 'user'))
async def add_user(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    existing = await database.check_user(data.id)
    if not existing:
        await database.add_user(data.first_name, data.last_name, data.username, data.id, role='user')
        await call.message.answer(text=f'Пользователю {data.first_name} {data.last_name} предоставлены права на просмотр')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'Ваша регистрация успешно пройдена, теперь Вы  можете просматривать карточки'\
                                 f' сотрудников НМИЦ гематологии, нажмите /start для начала работы')
    else:
        await database.edit_user_role(data.id, 'user')
        await call.message.answer(text=f'Права пользователя {data.first_name} {data.last_name} изменены на просмотр')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'доступ изменён, теперь Вы  можете просматривать карточки сотрудников НМИЦ гематологии. '\
                               f'Нажмите /start для начала работы')

@admins_router.callback_query(AdminCallback.filter(F.text == 'superuser'))
async def add_superuser(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    existing = await database.check_user(data.id)
    if not existing:
        await database.add_user(data.first_name, data.last_name, data.username, data.id, role='superuser')
        await call.message.answer(text=f'Пользователю {data.first_name} {data.last_name} предоставлены права на полный просмотр')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'Ваша регистрация успешно пройдена, теперь Вы  можете просматривать полные карточки'\
                                 f' сотрудников НМИЦ гематологии. Нажмите /start для начала работы')
    else:
        await database.edit_user_role(data.id, 'superuser')
        await call.message.answer(text=f'Права пользователя {data.first_name} {data.last_name} изменены на просмотр')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'доступ изменён, теперь Вы  можете просматривать полные карточки сотрудников НМИЦ гематологии. '\
                               f'Нажмите /start для начала работы')

@admins_router.callback_query(AdminCallback.filter(F.text == 'SED'))
async def add_sed_user(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    existing = await database.check_user(data.id)
    if not existing:
        await database.add_user(data.first_name, data.last_name, data.username, data.id, role='sed')
        await call.message.answer(text=f'Пользователю {data.first_name} {data.last_name} предоставлены права на изменение информации о СЭД')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'Ваша регистрация успешно пройдена, теперь Вы  можете просматривать полные карточки'\
                                 f' сотрудников НМИЦ гематологии и изменять информацию о доступе в СЭД. '\
                                    f'Нажмите /start для начала работы')
    else:
        await database.edit_user_role(data.id, 'sed')
        await call.message.answer(text=f'Права пользователя {data.first_name} {data.last_name} изменены на изменение информации о СЭД')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'доступ изменён, теперь Вы  можете просматривать полные карточки сотрудников НМИЦ гематологии '\
                                f'и изменять информацию о доступе в СЭД. Нажмите /start для начала работы')

@admins_router.callback_query(AdminCallback.filter(F.text == 'one_s'))
async def add_sed_user(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    existing = await database.check_user(data.id)
    if not existing:
        await database.add_user(data.first_name, data.last_name, data.username, data.id, role='one_s')
        await call.message.answer(text=f'Пользователю {data.first_name} {data.last_name} предоставлены права на изменение информации об 1С')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'Ваша регистрация успешно пройдена, теперь Вы  можете просматривать полные карточки'\
                                 f' сотрудников НМИЦ гематологии и изменять информацию о доступе в базы 1С. '\
                                    f'Нажмите /start для начала работы')
    else:
        await database.edit_user_role(data.id, 'one_s')
        await call.message.answer(text=f'Права пользователя {data.first_name} {data.last_name} изменены на изменение информации о 1C')
        await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                               f'доступ изменён, теперь Вы  можете просматривать полные карточки сотрудников НМИЦ гематологии '\
                                f'и изменять информацию о доступе в 1C. Нажмите /start для начала работы')

@admins_router.callback_query(AdminCallback.filter(F.text == 'reject_user'))
async def reject_user(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    await bot.send_message(chat_id=user_id, text=f'Уважаемый пользователь {data.first_name} {data.last_name},'\
                           f'Ваша регистрация отклонена')

@admins_router.callback_query(AdminCallback.filter(F.text == 'add_blacklist'))
async def add_blacklist(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    existing = await database.check_user(data.id)
    if not existing:
        await database.add_user(data.first_name, data.last_name, data.username, data.id, role='barbarian')
    await database.ban_user(data.id)
    await call.message.answer(text=f'Пользователь {data.first_name} {data.last_name} забанен')
        
    

@admins_router.callback_query(AdminCallback.filter(F.text == 'remove_blacklist'))
async def add_blacklist(call: types.CallbackQuery):
    id = call.message.text.split('^')
    user_id = int(id[0])
    data = await bot.get_chat(user_id)
    try:
        await database.unban_user(data.id)
        await call.message.answer(text=f'Пользователь {data.first_name} {data.last_name} разбанен')
    except:
        await call.message.answer(text=f'Пользователь {data.first_name} {data.last_name} в базе не числится')