#Файл функций для пользователя (просмотр данных без права редактирования)

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from states import View_Worker
from handlers.main import DBCommands
from keyboards.admins_keys import admin_keyboard, cancel_keyboard, one_plus_keuboard, security_keyboard
from keyboards.users_keys import UserCallback, user_keyboard

database = DBCommands()

users_router = Router(name=__name__)

@users_router.callback_query(UserCallback.filter(F.text == "see_worker"))
async def get_info_worker(call: types.CallbackQuery, state: FSMContext):
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        await state.set_state(View_Worker.name)
        await call.message.answer(text="Введите полностью или частично ФИО пользователя или нажмите отмену",
                         reply_markup=cancel_keyboard)
    else:
        await call.message.answer(text=f'Вы - незарегистрированный пользователь, '\
                               f'нажмите /registration для регистрации и получения доступа к матрице')

@users_router.message(View_Worker.name)
async def view_worker(message: types.Message):
    user = message.from_user.id
    is_user = await database.check_user(user)
    if is_user:
        role = await database.check_user_role(user)
        result = await database.view_worker(message.text, user, role)
        if result:
            if role == 'admin':
                await message.answer(
                    text='Поиск по базе данных окончен', reply_markup=admin_keyboard
                )
            elif role == 'one_s':
                await message.answer(
                    text='Поиск по базе данных окончен', reply_markup=one_plus_keuboard
                )
            elif role == 'security':
                await message.answer(
                    text='Поиск по базе данных окончен', reply_markup=security_keyboard
                )
            else:
                await message.answer(text='Поиск по базе данных окончен', reply_markup=user_keyboard) 