from keyboards.admins_keys import EditCallback, AdminCallback, edit_keyboard
from aiogram import types, F, Router
from handlers.main import DBCommands
from aiogram.fsm.context import FSMContext
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

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
    await call.message.answer(
        text='Данные внесены', reply_markup=edit_keyboard
    )



@admins_router.callback_query(AdminCallback.filter(F.text == 'edit_worker'))
async def get_worker_name(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Edit_Worker.name)
    await call.message.answer(text="Какого пользователя хотите скорректировать?",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

@editor_router.message(Edit_Worker.name)
async def get_id_for_names(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    buttons = []
    bool_worker = await database.view_worker_with_id(message.text, chat_id)
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
        await message.answer(text="Такого пользователя не найдено, повторите ввод",
                     reply_markup=types.ReplyKeyboardRemove()
                     )

@editor_router.callback_query(Edit_Worker.id)
async def add_func_for_worker(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.update_data(id=call.data[7::])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls['rm'])
        else:
            items_list.append(items['no'])
            calls_list.append(calls['plus'])
    await call.message.answer(
        text='Выберите из списка',
        reply_markup=edit_keyboard
    )


@admins_router.callback_query(AdminCallback.filter(F.text == "plus_apteka"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_apteka(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls['rm'])
        else:
            items_list.append(items['no'])
            calls_list.append(calls['plus'])
    await call.message.answer(
        text='Выберите из списка',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=
                          [
                              [
                              InlineKeyboardButton(text=f"{items_list[0]} Аптека",callback_data=AdminCallback(text=f"{calls_list[0]}apteka").pack()),
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
                          )
    )
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_zkgu"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_zkgu(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_bgu1"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_bgu1(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_bgu2"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_bgu2(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_dieta"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_dieta(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_mis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_MIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete() 

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_tis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_TIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "plus_sed"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.plus_SED(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_apteka"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_apteka(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_zkgu"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_zkgu(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_bgu1"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_bgu1(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_bgu2"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_bgu2(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_dieta"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_dieta(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_mis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_MIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_tis"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_TIS(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text == "rm_sed"))
async def plus_apteka(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_SED(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
    await call.message.delete()

@admins_router.callback_query(AdminCallback.filter(F.text =='email'))
async def complete(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Worker.email)
    await call.message.answer(
                         text="Введите актуальный почтовый адрес",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

@admins_router.message(Worker.email)
async def edit_email(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    person_id = await state.get_data()
    email = message.text
    await database.edit_email(int(person_id['id']), email)
    await message.answer(text='Адрес добавлен',
                         reply_markup=edit_keyboard
                         )

@admins_router.callback_query(AdminCallback.filter(F.text =='IS'))
async def complete(call: types.CallbackQuery, state: FSMContext):
    person_id = await state.get_data()
    await database.del_SED(person_id['id'])
    person_data = await database.view_worker_for_edition(int(person_id['id']))
    list_of_acc = list(person_data.values())
    items_list = []
    calls_list = []
    for acc in list_of_acc[1::]:
        if acc == 'Да':
            items_list.append(items['yes'])
            calls_list.append(calls["rm"])
        else:
            items_list.append(items['no'])
            calls_list.append(calls["plus"])
    await call.message.answer(
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
