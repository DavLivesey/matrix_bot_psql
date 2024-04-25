from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import callback_data
from .users_keys import UserCallback


class AdminCallback(callback_data.CallbackData, prefix='admin'):
    text: str

class AdminDeleteCallback(callback_data.CallbackData, prefix='delete'):
    text: str

class EditCallback(callback_data.CallbackData, prefix='editor'):
    text: str

class SertCallback(callback_data.CallbackData, prefix='sertificat'):
    text: str

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
    [  
        InlineKeyboardButton(text="Создать пользователя", callback_data=AdminCallback(text='add_worker').pack()),
        InlineKeyboardButton(text="Посмотреть пользователя", callback_data=UserCallback(text='see_worker').pack())
    ],
    [
        InlineKeyboardButton(text="Редактировать пользователя", callback_data=AdminCallback(text="edit_worker").pack()),
        InlineKeyboardButton(text='Удалить пользователя', callback_data=AdminDeleteCallback(text='delete_worker').pack())
    ],
    [
        InlineKeyboardButton(text='Посмотреть кончающиеся сертификаты', callback_data=AdminCallback(text='end_sert').pack())
    ]
    ]
    )


edit_keyboard = InlineKeyboardMarkup(inline_keyboard=
                                     [
                                         [
                                             InlineKeyboardButton(text='Информационные системы', callback_data=AdminCallback(text='IS').pack()),
                                             InlineKeyboardButton(text='Почтовый адрес', callback_data=AdminCallback(text='email').pack()),
                                             InlineKeyboardButton(text='ЭЦП', callback_data=SertCallback(text='ecp').pack()),
                                         ],
                                         [
                                             InlineKeyboardButton(text='Изменить отделение/отдел', callback_data=AdminCallback(text='edit_dep').pack()),
                                             InlineKeyboardButton(text='Изменить номер телефона', callback_data=AdminCallback(text='edit_phone').pack()),
                                         ],
                                         [
                                             InlineKeyboardButton(text="В начало",callback_data=AdminCallback(text="cancel").pack())
                                         ]
                                     ]
                                     )