from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from config import ADMIN_LIST
from states import View_Worker
from handlers.main import DBCommands
from keyboards.admins_keys import admin_keyboard
from keyboards.users_keys import UserCallback, user_keyboard

database = DBCommands()

users_router = Router(name=__name__)

@users_router.callback_query(UserCallback.filter(F.text == "see_worker"))
async def get_info_worker(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(View_Worker.name)
    await call.message.answer(text="Введите ФИО пользователя",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

@users_router.message(View_Worker.name)
async def add_Apteka(message: types.Message):
    user = message.from_user.id
    await database.view_worker(message.text, user)
    if user in ADMIN_LIST:
        await message.answer(text='Поиск по базе данных окончен', reply_markup=admin_keyboard)
    else:
        await message.answer(text='Поиск по базе данных окончен', reply_markup=user_keyboard) 