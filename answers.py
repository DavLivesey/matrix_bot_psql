from loader import bot

async def answer_incorrect_role(chat):
    await bot.send_message(chat_id=chat, text='У Вас недостаточно прав на это действие, '\
                              'вернитесь в начало командой /start')

async def answer_none_registration(chat):
    await bot.send_message(chat_id=chat, text=f'Вы - незарегистрированный пользователь, '\
                               f'нажмите /registration для регистрации и получения доступа к матрице')