#Файл функций изменения информации о доступах

from keyboards.admins_keys import EditCallback, AdminCallback, \
        edit_keyboard, cancel_keyboard, is_edit_keyboard, one_plus_keuboard, security_keyboard
from aiogram import types, F, Router
from handlers.main import DBCommands
from aiogram.fsm.context import FSMContext
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from answers import answer_incorrect_role, answer_none_registration
from loader import bot

from states import Edit_Worker, Worker

database = DBCommands()

items = {
    'yes': "✅ ",
    'no': "🚫 "
}
calls = {
    'rm': "rm_",
    'plus': "plus_"
}

admins_router = Router(name=__name__)
editor_router = Router(name=__name__)

@admins_router.callback_query(AdminCallback.filter(F.text =='complete'))
async def complete(call: types.CallbackQuery):
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        role = await database.check_user_role(user.id)
        if role == 'admin':
            await call.message.answer(
                text='✅ Данные внесены', reply_markup=edit_keyboard
            )
        elif role == 'one_s':
            await call.message.answer(
                text='✅ Данные внесены', reply_markup=one_plus_keuboard
            )
        elif role == 'security':
            await call.message.answer(
                text='✅ Данные внесены', reply_markup=security_keyboard
            )




@admins_router.callback_query(AdminCallback.filter(F.text == 'edit_worker'))
async def get_worker_name(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        await state.set_state(Edit_Worker.name)
        await call.message.answer(text="Какого пользователя хотите скорректировать?",
                             reply_markup=types.ReplyKeyboardRemove()
                             )
    else:
        await answer_none_registration(user.id)

@editor_router.message(Edit_Worker.name)
async def get_id_for_names(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    buttons = []
    is_user = await database.check_user(chat_id)
    if is_user:
        role = await database.check_user_role(chat_id)
        bool_worker = await database.view_worker_with_id(message.text, chat_id, role)
        if bool_worker != False:
            for person in bool_worker:
                buttons.append(InlineKeyboardButton(text=f"{person}",callback_data=EditCallback(text=f"{person}").pack()))
            await state.set_state(Edit_Worker.id)
            await message.answer(
                text='Нажмите ID выбранного пользователя',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=
                                                                   [
                                                                       buttons
                                                                   ])
                                                                   )
        else:
            await message.answer(text="Такого пользователя не найдено, повторите ввод или нажмите отмену",
                         reply_markup=cancel_keyboard)

@editor_router.callback_query(Edit_Worker.id)
async def add_func_for_worker(call: types.CallbackQuery, state: FSMContext):
    user = call.message.chat
    role = await database.check_user_role(user.id)
    await state.update_data(id=call.data[7::])
    person_id = call.data[7::]
    person_data = await database.view_worker_for_edition(person_id)
    list_of_acc = list(person_data.values())
    if role == 'admin':
        await call.message.answer(
            text='Выберите из списка',
            reply_markup=edit_keyboard
        )
    elif role == 'security':
        await call.message.answer(
            text='Выберите из списка',
            reply_markup=is_edit_keyboard
        )
    elif role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    else:
        await answer_incorrect_role(user.id)

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_apteka"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_apteka(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_zkgu"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_zkgu(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_bgu1"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_bgu1(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_bgu2"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_bgu2(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_dieta"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_dieta(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_mis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_MIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_tis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_TIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_sed"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_SED(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_apteka"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_apteka(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_zkgu"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_zkgu(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_bgu1"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_bgu1(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_bgu2"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_bgu2(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_dieta"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_dieta(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_mis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_MIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_tis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_TIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_sed"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_SED(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text =='email'))
async def complete(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Worker.email)
    await call.message.answer(
                         text="Введите актуальный почтовый адрес  или нажмите отмену",
                         reply_markup=cancel_keyboard)

@admins_router.message(Worker.email)
async def edit_email(message: types.Message, state: FSMContext):
    person_id = await state.get_data()
    email = message.text
    await database.edit_email(int(person_id['id']), email)
    await message.answer(text='Адрес добавлен',
                         reply_markup=edit_keyboard
                         )

@admins_router.callback_query(AdminCallback.filter(F.text =='ad'))
async def get_ad_row(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Worker.ad)
    await call.message.answer(
                         text="Введите учётную запись Active Directory или нажмите отмену",
                         reply_markup=cancel_keyboard)

@admins_router.message(Worker.ad)
async def add_ad(message: types.Message, state: FSMContext):
    person_id = await state.get_data()
    ad = message.text
    await database.add_ad(int(person_id['id']), ad)
    await message.answer(text='Адрес добавлен',
                         reply_markup=edit_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text =='IS'))
async def complete(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    user_role = await database.check_user_role(call.message.chat.id)
    if user_role == 'admin':
        await full_keyboard(list_of_acc, call.message.chat.id)
    elif user_role == 'one_s':
        await one_plus_actions(list_of_acc, call.message.chat.id)


async def full_keyboard(list_values, chat):
    items_list = []
    calls_list = []
    for acc in list_values[1::]:
        if acc == 'Нет' or acc == '':
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
        else:            
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
    await bot.send_message(chat_id=chat,
        text='Выберите из списка',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=
                          [
                              [
                              InlineKeyboardButton(text=f"{items_list[0]}Аптека",callback_data=AdminCallback(text=f"{calls_list[0]}apteka").pack()),
                              InlineKeyboardButton(text=f"{items_list[1]}Кадры",callback_data=AdminCallback(text=f"{calls_list[1]}zkgu").pack()),
                              InlineKeyboardButton(text=f"{items_list[2]}БГУ 1.0",callback_data=AdminCallback(text=f"{calls_list[2]}bgu1").pack()),
                              InlineKeyboardButton(text=f"{items_list[3]}БГУ 2.0",callback_data=AdminCallback(text=f"{calls_list[3]}bgu2").pack())
                              ],
                              [
                              InlineKeyboardButton(text=f"{items_list[4]}Диетпитание",callback_data=AdminCallback(text=f"{calls_list[4]}dieta").pack()),
                              InlineKeyboardButton(text=f"{items_list[5]}МИС",callback_data=AdminCallback(text=f"{calls_list[5]}mis").pack()),
                              InlineKeyboardButton(text=f"{items_list[6]}ТИС",callback_data=AdminCallback(text=f"{calls_list[6]}tis").pack()),
                              InlineKeyboardButton(text=f"{items_list[7]}СЭД",callback_data=AdminCallback(text=f"{calls_list[7]}sed").pack())
                              ],
                              [
                              InlineKeyboardButton(text="Готово",callback_data=AdminCallback(text="complete").pack()),
                              InlineKeyboardButton(text="В начало",callback_data=AdminCallback(text="cancel").pack())
                              ]
                          ]
                          ))

async def one_plus_actions(list_values, chat):
    items_list = []
    calls_list = []
    for acc in list_values[1::]:
        if acc == 'Нет' or acc == '':
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
        else:            
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
    await bot.send_message(chat_id=chat,
        text='Выберите из списка',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=
                          [
                              [
                              InlineKeyboardButton(text=f"{items_list[0]}Аптека",callback_data=AdminCallback(text=f"{calls_list[0]}apteka").pack()),
                              InlineKeyboardButton(text=f"{items_list[1]}Кадры",callback_data=AdminCallback(text=f"{calls_list[1]}zkgu").pack())
                              ],
                              [
                              InlineKeyboardButton(text=f"{items_list[2]}БГУ 1.0",callback_data=AdminCallback(text=f"{calls_list[2]}bgu1").pack()),
                              InlineKeyboardButton(text=f"{items_list[3]}БГУ 2.0",callback_data=AdminCallback(text=f"{calls_list[3]}bgu2").pack()),
                              InlineKeyboardButton(text=f"{items_list[4]}Диетпитание",callback_data=AdminCallback(text=f"{calls_list[4]}dieta").pack())
                              ],
                              [
                              InlineKeyboardButton(text="Готово",callback_data=AdminCallback(text="complete").pack()),
                              InlineKeyboardButton(text="В начало",callback_data=AdminCallback(text="cancel").pack())
                              ]
                          ]
                          ))