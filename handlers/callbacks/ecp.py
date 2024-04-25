from datetime import date
import datetime
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import logging, operator
from config import ADMIN_LIST, ADMIN_CHAT
from states import Worker, Ex_Worker, Edit_Worker, sertificate
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from keyboards.admins_keys import admin_keyboard, AdminCallback, SertCallback
from handlers.main import DBCommands
from loader import bot
from aiogram.enums import ParseMode

database = DBCommands()

sertificate_router = Router(name=__name__)

@sertificate_router.callback_query(SertCallback.filter(F.text == "ecp"))
async def create_new_sert_type(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(sertificate.sert_type)
    await call.message.answer(text="Выберите тип УЦ",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text='Контур', callback_data=SertCallback(text='Контур').pack()),
                                     InlineKeyboardButton(text='УФК', callback_data=SertCallback(text='УФК').pack())
                                 ]
                             ]
                         )
                         )

@sertificate_router.callback_query(sertificate.sert_type)
async def create_new_sert_serial(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(sert_type = call.data[11::])
    await state.set_state(sertificate.serial_number)
    await call.message.answer(text="Введите серийный номер сертификата",
                         reply_markup=types.ReplyKeyboardRemove())

@sertificate_router.message(sertificate.serial_number)
async def create_new_sert_start(message: types.Message, state: FSMContext):
    await state.update_data(serial_number = message.text)
    await state.set_state(sertificate.date_start)
    await message.answer(text="Введите дату начала действия сертификата в формате год, месяц, день без разделителей (8 знаков)",
                         reply_markup=types.ReplyKeyboardRemove())

@sertificate_router.message(sertificate.date_start)
async def create_new_sert_fin(message: types.Message, state: FSMContext):
    await state.update_data(date_start = message.text)
    await state.set_state(sertificate.date_finish)
    await message.answer(text="Введите дату окончания действия сертификата в формате год, месяц, день без разделителей (8 знаков)",
                         reply_markup=types.ReplyKeyboardRemove())

@sertificate_router.message(sertificate.date_finish)
async def insert_sert_in_database(message: types.Message, state: FSMContext):
    await state.update_data(date_finish = message.text)
    data = await state.get_data()
    result = await database.add_new_sert(worker_id=str(data["id"]), center_name=str(data["sert_type"]), \
                                         serial_number=str(data["serial_number"]), date_start=datetime.datetime.strptime(str(data["date_start"]), "%Y%m%d"), \
                                            date_finish=datetime.datetime.strptime(str(data["date_finish"]), "%Y%m%d"))
    await message.answer(text="Данные по сертификату успешно внесены",
                         reply_markup=admin_keyboard)