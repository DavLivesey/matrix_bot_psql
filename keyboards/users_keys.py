from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import callback_data


class UserCallback(callback_data.CallbackData, prefix='user'):
    text: str

user_keyboard = InlineKeyboardMarkup(inline_keyboard=
                                     [
                                         [InlineKeyboardButton(text="Посмотреть пользователя",
                                                               callback_data=UserCallback(text='see_worker').pack()
                                                               )
                                                               ]])
