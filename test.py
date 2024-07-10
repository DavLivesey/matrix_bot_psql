from handlers.main import DBCommands
import asyncio

db = DBCommands()

async def get_mails():
    workers_list = await db.get_all_workers()
    for worker in workers_list:
        await db.get_old_mailbox(worker[0])
    print('Успешно')


if __name__ == "__main__":
    asyncio.run(get_mails())