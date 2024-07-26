from datetime import date
import datetime
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import logging, operator
from config import ADMIN_CHAT
from states import Worker, Ex_Worker, Edit_Worker, sertificate
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from keyboards.admins_keys import admin_keyboard, AdminCallback, \
            SertCallback, cancel_keyboard, cancel_button, security_keyboard
from handlers.main import DBCommands
from loader import bot
from aiogram.enums import ParseMode
from handlers.callbacks.admins import admins_router
from answers import answer_incorrect_role, answer_none_registration

database = DBCommands()

sertificate_router = Router(name=__name__)

@sertificate_router.callback_query(SertCallback.filter(F.text == "ecp"))
async def create_new_sert_type(call: types.CallbackQuery, state: FSMContext):
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        role = await database.check_user_role(user.id)
        if role == 'admin' or role == 'security':
            await state.set_state(sertificate.sert_type)
            await call.message.answer(text="Выберите тип УЦ",
                                 reply_markup=InlineKeyboardMarkup(
                                     inline_keyboard=[
                                        [
                                           InlineKeyboardButton(text='Контур', callback_data=SertCallback(text='Контур').pack()),
                                           InlineKeyboardButton(text='УФК', callback_data=SertCallback(text='УФК').pack())
                                        ],
                                        [
                                            cancel_button
                                        ]
                                     ]
                                 )
                                 )
        else:
            await answer_incorrect_role(user.id)
    else:
        await answer_none_registration(user.id)

@sertificate_router.callback_query(sertificate.sert_type)
async def create_new_sert_serial(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(sert_type = call.data[11::])
    await state.set_state(sertificate.serial_number)
    await call.message.answer(text="Введите серийный номер сертификата или нажмите отмену",
                         reply_markup=cancel_keyboard)

@sertificate_router.message(sertificate.serial_number)
async def create_new_sert_start(message: types.Message, state: FSMContext):
    await state.update_data(serial_number = message.text)
    await state.set_state(sertificate.date_start)
    await message.answer(text="Введите дату начала действия сертификата или нажмите отмену",
                         reply_markup=cancel_keyboard)

@sertificate_router.message(sertificate.date_start)
async def create_new_sert_fin(message: types.Message, state: FSMContext):
    await state.update_data(date_start = message.text)
    await state.set_state(sertificate.date_finish)
    await message.answer(text="Введите дату окончания действия сертификата или нажмите отмену",
                         reply_markup=cancel_keyboard)

@sertificate_router.message(sertificate.date_finish)
async def insert_sert_in_database(message: types.Message, state: FSMContext):
    await state.update_data(date_finish = message.text)
    user = message.chat
    role = await database.check_user_role(user.id)
    data = await state.get_data()
    await database.add_new_sert(
                                        worker_id=str(data["id"]), center_name=str(data["sert_type"]), \
                                        serial_number=str(data["serial_number"]), \
                                        date_start=datetime.datetime.strptime(data["date_start"], '%d%m%Y').date(), \
                                        date_finish=datetime.datetime.strptime(data["date_finish"], '%d%m%Y').date()
                                        )
    if role == 'admin':
            await message.answer(text="Данные по сертификату успешно внесены",
                         reply_markup=admin_keyboard)
    elif role == 'security':
            await message.answer(text="Данные по сертификату успешно внесены",
                         reply_markup=security_keyboard)
    else:
        await answer_incorrect_role(user.id)

@admins_router.callback_query(AdminCallback.filter(F.text == 'end_sert'))
async def get_ending_serts(call: types.CallbackQuery):
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        role = await database.check_user_role(user.id)
        chat_id = call.from_user.id
        await database.sert_ends(chat_id)
        if role == 'admin':
            await call.message.answer(text='Поиск окончен', reply_markup=admin_keyboard)
        elif role == 'security':
            await call.message.answer(text='Поиск окончен', reply_markup=security_keyboard)
    else:
        await answer_none_registration(user.id)

@sertificate_router.callback_query(SertCallback.filter(F.text == 'pass_flesh'))
async def pass_flesh(call: types.CallbackQuery, state: FSMContext):
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
            await call.message.answer(text='Вы уверены, что ЭЦП сданы?', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text='Да, это абсолютно точно', callback_data=SertCallback(text='confirm_delete_ecp').pack()),
                                                                InlineKeyboardButton(text='Ой, нет, я передумал', callback_data=AdminCallback(text="cancel").pack())
                                                            ]
]))
    else:
        await answer_none_registration(user.id)

@sertificate_router.callback_query(SertCallback.filter(F.text == 'confirm_delete_ecp'))
async def pass_flesh(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = call.message.chat
    role = await database.check_user_role(user.id)
    await database.pass_ecp(int(data['id']))
    if role == 'admin':
            await call.message.answer(text='ЭЦП сданы', reply_markup=admin_keyboard)
    elif role == 'security':
            await call.message.answer(text='ЭЦП сданы', reply_markup=security_keyboard)
    else:
        await answer_incorrect_role(user.id)