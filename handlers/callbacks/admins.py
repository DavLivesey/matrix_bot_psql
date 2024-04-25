from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import logging, operator
from config import ADMIN_LIST, ADMIN_CHAT
from states import Worker, Ex_Worker, Edit_Worker
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from keyboards.admins_keys import admin_keyboard, AdminCallback, AdminDeleteCallback
from handlers.main import DBCommands
from loader import bot
from aiogram.enums import ParseMode

database = DBCommands()

items = {
    'yes': "✅ ",
    'no': "🚫 "
}

calls = {
    'rm': "rm_",
    'plus': "plus_"
}

logging.basicConfig(format=u'%(filename)s [LINE:%(lineНет)d] #%(levelname)-8s'
                           u'[%(asctime)s]  %(message)s',
                    level=logging.INFO)



admins_router = Router(name=__name__)
admins_del_router = Router(name=__name__)


@admins_router.callback_query((AdminCallback.filter(F.text == "cancel")))
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info("Отменено %r", current_state)
    await state.clear()
    await call.message.answer(
        text='Данные внесены, дальнейшая работа над пользователем остановлена', reply_markup=admin_keyboard
    )

@admins_router.callback_query(AdminCallback.filter(F.text == "add_worker"))
async def create_new_worker(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Worker.name)
    await call.message.answer(text="Введите ФИО пользователя",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

@admins_router.message(Worker.name)
async def add_info_sys(message: types.Message, state: FSMContext):
    await database.add_new_worker(message.text)
    user = message.from_user.id
    autor = message.from_user
    await bot.send_message(chat_id=ADMIN_CHAT, text=f"Пользователь {autor.first_name} "\
                            f"{autor.last_name} под ником @{autor.username} создал запись о сотруднике {message.text}",
                              parse_mode=ParseMode.HTML)
    person_data = await database.check_worker(message.text, user)
    await state.update_data(id=person_data[0])
    items_list = []
    calls_list = []
    for acc in person_data[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls['rm'])
        else:
            items_list.append(items['no'])
            calls_list.append(calls['plus'])
    await message.answer(
        text='Выберите из списка',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=
                          [
                              [
                              InlineKeyboardButton(text=f"{items_list[0]} Аптека",callback_data=AdminCallback(text=f"{calls_list[0]}apteka").pack()),
                              InlineKeyboardButton(text=f"{items_list[1]}Кадры",callback_data=AdminCallback(text=f"{calls_list[1]}zkgu").pack()),
                              InlineKeyboardButton(text=f"{items_list[2]}БГУ 1.0",callback_data=AdminCallback(text=f"{calls_list[2]}bgu1").pack()),
                              InlineKeyboardButton(text=f"{items_list[3]}БГУ 2.0",callback_data=AdminCallback(text=f"{calls_list[3]}bgu2").pack()),
                              ],
                              [
                              InlineKeyboardButton(text=f"{items_list[4]}Диетпитание",callback_data=AdminCallback(text=f"{calls_list[4]}dieta").pack()),
                              InlineKeyboardButton(text=f"{items_list[5]}МИС",callback_data=AdminCallback(text=f"{calls_list[5]}mis").pack()),
                              InlineKeyboardButton(text=f"{items_list[6]}ТИС",callback_data=AdminCallback(text=f"{calls_list[6]}tis").pack()),
                              InlineKeyboardButton(text=f"{items_list[7]}СЭД",callback_data=AdminCallback(text=f"{calls_list[7]}sed").pack()),
                              ],
                              [
                              InlineKeyboardButton(text="Готово",callback_data=AdminCallback(text="complete").pack()),
                              InlineKeyboardButton(text="В начало",callback_data=AdminCallback(text="cancel").pack())
                              ]
                          ]
                          )
    )

@admins_del_router.callback_query(AdminDeleteCallback.filter(F.text == "delete_worker"))
async def check_worker_name(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Ex_Worker.name)
    await call.message.answer(text="Какого пользователя хотите удалить?",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

@admins_del_router.message(Ex_Worker.name)
async def get_id_for_names(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    buttons = []
    bool_worker = await database.view_worker_with_id(message.text, chat_id)
    autor = message.from_user
    await bot.send_message(chat_id=ADMIN_CHAT, text=f"Пользователь {autor.first_name} "\
                            f"{autor.last_name} под ником @{autor.username} создал запись о сотруднике {message.text}",
                              parse_mode=ParseMode.HTML)
    if bool_worker != False:
        for person in bool_worker:
            buttons.append(InlineKeyboardButton(text=f"{person}",callback_data=AdminCallback(text=f"{person}").pack()))
        await state.set_state(Ex_Worker.id)
        await message.answer(
            text='Нажмите ID выбранного пользователя',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=
                                                               [
                                                                   buttons
                                                               ])
                                                               )
    else:
        await message.answer(text="Такого пользователя не найдено, повторите ввод",
                     reply_markup=types.ReplyKeyboardRemove()
                     )

@admins_del_router.callback_query(Ex_Worker.id)
async def get_id_for_names(call: types.CallbackQuery):
    result = await database.del_worker(call.data[6::])
    if result ==True:
        await call.message.answer(text='Пользователь успешно удален', reply_markup=admin_keyboard)
    else:
        await call.message.answer(text='Что-то пошло не так, попробуйте ещё раз', reply_markup=admin_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text == 'end_sert'))
async def get_ending_serts(call: types.CallbackQuery):
    chat_id = call.from_user.id
    await database.sert_ends(chat_id)
    await call.message.answer(text='Поиск окончен', reply_markup=admin_keyboard
                       )

@admins_router.callback_query(AdminCallback.filter(F.text == 'edit_dep'))
async def add_dep(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Worker.department)
    await call.message.answer(text="Введите название отделения",
                     reply_markup=types.ReplyKeyboardRemove()
                       )

@admins_router.message(Worker.department)
async def add_dep(message: types.Message, state:FSMContext):
    chat_id = message.from_user.id
    data = await state.get_data()
    worker_id = data['id']
    worker_dep = message.text
    await database.add_department(worker_id, chat_id, worker_dep)
    await message.answer(text='Подразделение добавлено', reply_markup=admin_keyboard
                       )

@admins_router.callback_query(AdminCallback.filter(F.text == 'edit_phone'))
async def add_dep(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Worker.phone)
    await call.message.answer(text="Введите новый номер телефона",
                     reply_markup=types.ReplyKeyboardRemove()
                        )

@admins_router.message(Worker.phone)
async def add_dep(message: types.Message, state:FSMContext):
    data = await state.get_data()
    worker_id = data['id']
    worker_phone = message.text
    await database.add_telephone(worker_id, worker_phone)
    await message.answer(text='Телефон обновлен', reply_markup=admin_keyboard
                       )