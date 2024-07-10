from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
import logging
from config import ADMIN_CHAT
from states import Worker, Ex_Worker, Workplace
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from keyboards.admins_keys import admin_keyboard, AdminCallback, \
        AdminDeleteCallback, edit_keyboard, cancel_keyboard, \
            cancel_button, one_plus_keuboard, security_keyboard, \
            edit_dep_keyboard, edit_mailbox, edit_phone
from keyboards.users_keys import user_keyboard
from handlers.main import DBCommands
from loader import bot
from aiogram.enums import ParseMode
from answers import answer_incorrect_role, answer_none_registration

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
    await state.clear()
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        role = await database.check_user_role(user.id)
        if role == 'admin':
            await call.message.answer(
                text='Данные внесены, дальнейшая работа над пользователем остановлена', reply_markup=admin_keyboard)
        elif role == 'one_s':
            await call.message.answer(
                text='Данные внесены, дальнейшая работа над пользователем остановлена', reply_markup=one_plus_keuboard)
        elif role == 'security':
            await call.message.answer(
                text='Данные внесены, дальнейшая работа над пользователем остановлена', reply_markup=security_keyboard)
        else:
            await call.message.answer(
                text='Данные внесены, дальнейшая работа над пользователем остановлена', reply_markup=user_keyboard)
    

@admins_router.callback_query(AdminCallback.filter(F.text == "add_worker"))
async def create_new_worker(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        role = await database.check_user_role(user.id)
        if role == 'admin':
            await state.set_state(Worker.name)
            await call.message.answer(text="Введите ФИО пользователя",
                                 reply_markup=types.ReplyKeyboardRemove()
                                 )
        else:
            await answer_incorrect_role(user.id)
    else:
        await answer_none_registration(user.id)

@admins_router.callback_query(AdminCallback.filter(F.text == "edit_fio"))
async def edit_fio(call: types.CallbackQuery, state: FSMContext):
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:       
        role = await database.check_user_role(call.message.chat.id)
        if role == 'admin':
                await state.set_state(Worker.new_name)
                await call.message.answer(text="Введите новые ФИО пользователя",
                                     reply_markup=types.ReplyKeyboardRemove()
                                     )
        else:
            await answer_incorrect_role(user.id)
    else:
        await answer_none_registration(user.id)

@admins_router.message(Worker.new_name)
async def update_fio(message: types.Message, state: FSMContext):    
    data = await state.get_data()
    worker_id = data['id']
    result = await database.view_worker_for_edition(worker_id)
    old_fio = result['name']
    await database.edit_fio(worker_id, message.text)
    await message.answer(
                text=f'ФИО изменено с {old_fio} на {message.text}', reply_markup=admin_keyboard)

@admins_router.message(Worker.name)
async def add_info_sys(message: types.Message, state: FSMContext):
    adding = await database.add_new_worker(message.text, message.from_user.id)
    if adding==True:
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
    else:
        await message.answer(
        text='Проверьте правильность ФИО нового пользователя или отредактируйте текущего', reply_markup=admin_keyboard)

@admins_del_router.callback_query(AdminDeleteCallback.filter(F.text == "delete_worker"))
async def check_worker_name(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user = call.message.chat
    is_user = await database.check_user(user.id)
    if is_user:
        role = await database.check_user_role(user.id)
        if role == 'admin':
            await state.set_state(Ex_Worker.name)
            await call.message.answer(text="Введите полностью или частично ФИО пользователя или нажмите отмену",
                                 reply_markup=cancel_keyboard)
        else:
            await answer_incorrect_role(user.id)
    else:
        await answer_none_registration(user.id)
    

@admins_del_router.message(Ex_Worker.name)
async def get_id_for_names(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    buttons = []
    role = await database.check_user_role(chat_id)
    bool_worker = await database.view_worker_with_id(message.text, chat_id, role)
    if role == 'admin':
        if bool_worker != False:
            for person in bool_worker:
                buttons.append(InlineKeyboardButton(text=f"{person}",callback_data=AdminCallback(text=f"{person}").pack()))
            await state.set_state(Ex_Worker.id)
            await message.answer(
                text='Нажмите ID выбранного пользователя',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                                       buttons,
                                                                   [
                                                                       cancel_button
                                                                   ]]
                                                                   )
                                                                   )
        else:
            await message.answer(text="Такого пользователя не найдено, повторите ввод, либо нажмите отмену",
                         reply_markup=cancel_keyboard)
    else:
            await answer_incorrect_role(chat_id)

@admins_del_router.callback_query(Ex_Worker.id)
async def get_id_for_names(call: types.CallbackQuery, state: FSMContext):
    await database.view_worker_for_edition(call.data[6::])
    await database.get_worker_card(int(call.data[6::]), call.message.chat)
    result = await database.del_worker(call.data[6::])
    if result ==True:
        await call.message.answer(text='✅ Пользователь успешно удален', reply_markup=admin_keyboard)
        await state.clear()
    else:
        await call.message.answer(text='Что-то пошло не так, попробуйте ещё раз', reply_markup=admin_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text == 'edit_dep'))
async def choise_dep_edit(call: types.CallbackQuery):
    await call.message.answer(text="Добавляем или удаляем?",
                     reply_markup=edit_dep_keyboard)
    
@admins_router.callback_query(AdminCallback.filter(F.text == 'add_position'))
async def get_dep_name(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Workplace.department)
    await call.message.answer(text="Введите название подразделения или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Workplace.department)
async def get_position(message: types.Message, state:FSMContext):
    await state.update_data(department=message.text)
    await state.set_state(Workplace.position)
    await message.answer(text="Введите название должности или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Workplace.position)
async def add_dep_pos(message: types.Message, state:FSMContext):
    await state.update_data(position=message.text)
    data = await state.get_data()
    result = await database.join_position(data['id'], data['position'], data['department'])
    if result == 1:
        await message.answer(text="Такого подразделения не существует, попробуйте снова",
                     reply_markup=edit_keyboard)
    elif result == 2:
        await message.answer(text="Такой специальности не существует, попробуйте снова",
                     reply_markup=edit_keyboard)
    else:
        await message.answer(text="Пользователю добавлены должность и подразделение",
                         reply_markup=edit_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text == 'del_position'))
async def get_dep(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Workplace.old_dep)
    await call.message.answer(text="Введите название бывшего подразделения или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Workplace.old_dep)
async def get_position(message: types.Message, state:FSMContext):
    await state.update_data(old_dep=message.text)
    await state.set_state(Workplace.old_pos)
    await message.answer(text="Введите название бывшей должности или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Workplace.old_pos)
async def add_dep_pos(message: types.Message, state:FSMContext):
    await state.update_data(old_pos=message.text)
    data = await state.get_data()
    result = await database.leave_position(data['id'], data['old_pos'], data['old_dep'])
    if result == 1:
        await message.answer(text="Такого подразделения не существует, попробуйте снова",
                     reply_markup=edit_keyboard)
    elif result == 2:
        await message.answer(text="Такой специальности не существует, попробуйте снова",
                     reply_markup=edit_keyboard)
    else:
        await message.answer(text=f"Пользователь удален с должности {data['old_pos']} в {data['old_dep']}",
                         reply_markup=edit_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text == 'edit_phone'))
async def choise_phone(call: types.CallbackQuery):
    await call.message.answer(text="Добавляем или удаляем?",
                     reply_markup=edit_phone)

@admins_router.callback_query(AdminCallback.filter(F.text == 'add_phone'))
async def get_phone_number(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Worker.phone)
    await call.message.answer(text="Введите номер телефона или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Worker.phone)
async def add_phone(message: types.Message, state:FSMContext):
    data = await state.get_data()
    worker_id = data['id']
    worker_phone = message.text
    result = await database.add_telephone(worker_id, worker_phone)
    if result:
        await message.answer(text='Телефон обновлен', reply_markup=edit_keyboard)
    else:
        await message.answer(text=f'Телефон {worker_phone} имеет некорректный формат, попробуйте снова ии нажмите отмену', 
                        reply_markup=cancel_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text == 'del_phone'))
async def get_name_ex_phone(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Worker.ex_phone)
    await call.message.answer(text="Введите номер телефона или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Worker.ex_phone)
async def remove_phone(message: types.Message, state:FSMContext):
    data = await state.get_data()
    worker_id = data['id']
    ex_phone = message.text
    success = await database.remove_telephone(worker_id, ex_phone)
    if success:
        await message.answer(text='Телефон удален', reply_markup=edit_keyboard)
    else:
        await message.answer(text='Что-то пошло не так, попробуйте ещё раз или нажмите отмену',
                             reply_markup=cancel_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text == 'mailbox'))
async def choise_mailbox(call: types.CallbackQuery):
    await call.message.answer(text="Добавляем или удаляем?",
                     reply_markup=edit_mailbox)

@admins_router.callback_query(AdminCallback.filter(F.text == 'add_mailbox'))
async def get_name_mailbox(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Worker.mailbox)
    await call.message.answer(text="Введите название рассылки или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Worker.mailbox)
async def push_mailbox(message: types.Message, state:FSMContext):
    data = await state.get_data()
    worker_id = data['id']
    mailbox = message.text
    await database.add_mailbox(worker_id, mailbox)
    await message.answer(text='Рассылка добавлена', reply_markup=edit_keyboard)

@admins_router.callback_query(AdminCallback.filter(F.text == 'del_mailbox'))
async def get_name_ex_mailbox(call: types.CallbackQuery, state:FSMContext):
    await state.set_state(Worker.ex_mailbox)
    await call.message.answer(text="Введите название рассылки или нажмите отмену",
                     reply_markup=cancel_keyboard)

@admins_router.message(Worker.ex_mailbox)
async def remove_mailbox(message: types.Message, state:FSMContext):
    data = await state.get_data()
    worker_id = data['id']
    ex_mailbox = message.text
    await database.remove_mailbox(worker_id, ex_mailbox)
    await message.answer(text='Рассылка добавлена', reply_markup=edit_keyboard)


