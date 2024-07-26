import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
HOST = os.getenv('HOST')
PG_PSWD = os.getenv('PG_PSWD')
PG_USER = os.getenv('PG_USER')
ADMIN_CHAT = int(os.getenv('ADMIN_CHAT'))

