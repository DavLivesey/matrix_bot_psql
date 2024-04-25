import asyncio
import logging
import sqlite3
from config import HOST, PG_PSWD, PG_USER, PATH_TO_BASES, PROJECT_DESTINATION

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s'
                           u'[%(asctime)s]  %(message)s',
                    level=logging.INFO)

async def create_db():
    create_db_command = open(f'{PROJECT_DESTINATION}create_dbl.sql', 'r').read()
    logging.info('Connection to db...')
    conn = sqlite3.connect (f'{PATH_TO_BASES}workers.db')
    cur = conn.cursor()
    cur.executescript(create_db_command)
    logging.info('Table was created')
    conn.close()


async def create_pool():
    return sqlite3.connect(f'{PATH_TO_BASES}workers.db')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
    loop.run_until_complete(create_pool())
