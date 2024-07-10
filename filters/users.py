from aiogram.filters import BaseFilter
from aiogram.types import Message
from handlers.main import DBCommands

db = DBCommands()

class UserFilter(BaseFilter):
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    async def admin_user(self, message: Message) -> bool:
        role = await db.check_user_role(message.from_user.id)
        return role