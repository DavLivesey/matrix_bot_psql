#Пусковой скрипт бота
import asyncio
from loader import dp
from aiogram import Bot
from handlers import start
from handlers.callbacks import admins, users, \
            edit_access, ecp, admin_users
from config import BOT_TOKEN

async def main():
    bot = Bot(BOT_TOKEN)
    dp.include_router(start.router)
    dp.include_router(users.users_router)
    dp.include_router(admins.admins_router)
    dp.include_router(admins.admins_del_router)
    dp.include_router(ecp.sertificate_router)
    dp.include_router(edit_access.admins_router)
    dp.include_router(edit_access.editor_router)
    dp.include_router(admin_users.admins_router)

    
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())