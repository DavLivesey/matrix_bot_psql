#Модули состояний

from aiogram.fsm.state import StatesGroup, State

class Worker(StatesGroup):
    name = State()
    new_name = State()
    email = State()
    phone = State()
    ex_phone = State()
    mailbox = State()
    ex_mailbox = State()
    ad = State()

class Workplace(StatesGroup):
    department = State()
    position = State()
    old_dep = State()
    old_pos = State()

class View_Worker(StatesGroup):
    name = State()

class Ex_Worker(StatesGroup):
    id = State()
    name = State()

class Edit_Worker(StatesGroup):
    id = State()
    name = State()

class sertificate(StatesGroup):
    worker_id = State()
    sert_type = State()
    serial_number = State()
    worker_id = State()
    date_start = State()
    date_finish = State()

class User_Form(StatesGroup):
    firstname = State()
    lastname = State()
    username = State()
    user_id = State()
    role = State()