from aiogram.fsm.state import StatesGroup, State

class Worker(StatesGroup):
    name = State()
    email = State()
    department = State()
    phone = State()

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