import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_LIST = [int(os.getenv('ADMIN_1')), int(os.getenv('ADMIN_2')), \
              int(os.getenv('ADMIN_3')), int(os.getenv('ADMIN_4')), \
              int(os.getenv('ADMIN_5')), int(os.getenv('ADMIN_6')), \
              int(os.getenv('ADMIN_7'))]
HOST = os.getenv('HOST')
PG_PSWD = os.getenv('PG_PSWD')
PG_USER = os.getenv('PG_USER')
ADMIN_CHAT = int(os.getenv('ADMIN_CHAT'))
PATH_TO_BASES = os.getenv('PATH_TO_BASES')
PROJECT_DESTINATION = os.getenv('PROJECT_DESTINATION')

