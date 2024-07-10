#Файл с клавиатурами различных админских ролей

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import callback_data
from .users_keys import UserCallback

items_list = ['🚫', '🚫', '🚫', '🚫', '🚫', '🚫', '🚫', '🚫']
calls_list = ["plus", "plus", "plus", "plus", "plus", "plus", "plus", "plus"]

class AdminCallback(callback_data.CallbackData, prefix='admin'):
    text: str

class AdminDeleteCallback(callback_data.CallbackData, prefix='delete'):
    text: str

class EditCallback(callback_data.CallbackData, prefix='editor'):
    text: str

class SertCallback(callback_data.CallbackData, prefix='sertificat'):
    text: str

#основная клавиатура админов
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

#основная клавиатура редактирования карточки работника
edit_keyboard = InlineKeyboardMarkup(inline_keyboard=
                                     [
                                         [                                             
                                             InlineKeyboardButton(text='AD', callback_data=AdminCallback(text='ad').pack()),
                                             InlineKeyboardButton(text='Почта', callback_data=AdminCallback(text='email').pack()),
                                             InlineKeyboardButton(text='ИС', callback_data=AdminCallback(text='IS').pack()),
                                             InlineKeyboardButton(text='ЭЦП', callback_data=SertCallback(text='ecp').pack())                                             
                                         ],
                                         [
                                             InlineKeyboardButton(text='Подразделение', callback_data=AdminCallback(text='edit_dep').pack()),
                                             InlineKeyboardButton(text='Телефон', callback_data=AdminCallback(text='edit_phone').pack()),
                                         ],
                                         [                                             
                                             InlineKeyboardButton(text='Изменить ФИО сотрудника', callback_data=AdminCallback(text='edit_fio').pack()),
                                             InlineKeyboardButton(text='Почтовая рассылка', callback_data=AdminCallback(text='mailbox').pack())
                                         ],
                                         [   
                                             InlineKeyboardButton(text='Пользователь сдал ключ', callback_data=SertCallback(text='pass_flesh').pack()),
                                             InlineKeyboardButton(text="В начало",callback_data=AdminCallback(text="cancel").pack())
                                         ]
                                     ]
                                     )

#кнопка отмены
cancel_button = InlineKeyboardButton(text="❌ Отмена",callback_data=AdminCallback(text="cancel").pack())

#клавиатура отмены
cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=                                                                
                                                               [[
                                                                   cancel_button
                                                               ]]
                                                                )

#клавиатура для регистрации пользователя в админском чате
registration_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                [
                                                                    InlineKeyboardButton(text="Админ",callback_data=AdminCallback(text="admin").pack()),
                                                                    InlineKeyboardButton(text="ИБ",callback_data=AdminCallback(text="security").pack()),
                                                                    InlineKeyboardButton(text="Суперпользователь",callback_data=AdminCallback(text="superuser").pack())
                                                                ],
                                                                [
                                                                    InlineKeyboardButton(text="Пользователь",callback_data=AdminCallback(text="user").pack()),
                                                                    InlineKeyboardButton(text="1Сник",callback_data=AdminCallback(text="one_s").pack()),
                                                                    InlineKeyboardButton(text="Сэдовец",callback_data=AdminCallback(text="SED").pack())
                                                                ],
                                                                [
                                                                    InlineKeyboardButton(text="Отвергнуть",callback_data=AdminCallback(text="reject_user").pack()),
                                                                    InlineKeyboardButton(text="Бан",callback_data=AdminCallback(text="add_blacklist").pack()),
                                                                    InlineKeyboardButton(text="Разбан",callback_data=AdminCallback(text="remove_blacklist").pack())
                                                                ]
]
                                             )

#основная клавиатура для безопасников
security_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text="Редактировать пользователя", callback_data=AdminCallback(text="edit_worker").pack()),
                                                                InlineKeyboardButton(text="Посмотреть пользователя", callback_data=UserCallback(text='see_worker').pack())                                                                
                                                            ],
                                                            [
                                                                InlineKeyboardButton(text='Посмотреть кончающиеся сертификаты', callback_data=AdminCallback(text='end_sert').pack())
                                                            ]
])

#клавиатура редактирования пользователей для безопасников
is_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text='ЭЦП', callback_data=SertCallback(text='ecp').pack()),
                                                                InlineKeyboardButton(text='Пользователь сдал ключ', callback_data=SertCallback(text='pass_flesh').pack())
                                                            ],
                                                            [
                                                                InlineKeyboardButton(text="В начало",callback_data=AdminCallback(text="cancel").pack())
                                                            ]
]
                                        )


#основная клавиатура для 1С
one_plus_keuboard = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text="Редактировать пользователя", callback_data=AdminCallback(text="edit_worker").pack()),
                                                                InlineKeyboardButton(text="Посмотреть пользователя", callback_data=UserCallback(text='see_worker').pack())
                                                            ]])

#клавиатура для изменения подразделения и должности
edit_dep_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text='Добавить отдел/должность', callback_data=AdminCallback(text='add_position').pack()),
                                                                InlineKeyboardButton(text='Убрать отдел/должность', callback_data=AdminCallback(text='del_position').pack())
                                                            ],
                                                            [
                                                                cancel_button
                                                            ]
])

#клавиатура для изменения почтовых рассылок
edit_mailbox = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text='Добавить одну', callback_data=AdminCallback(text='add_mailbox').pack()),
                                                                InlineKeyboardButton(text='Убрать одну', callback_data=AdminCallback(text='del_mailbox').pack())
                                                            ],
                                                            [
                                                                cancel_button
                                                            ]
])

#клавиатура для изменения телефона
edit_phone = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text='Добавить', callback_data=AdminCallback(text='add_phone').pack()),
                                                                InlineKeyboardButton(text='Убрать', callback_data=AdminCallback(text='del_phone').pack())
                                                            ],
                                                            [
                                                                cancel_button
                                                            ]
])