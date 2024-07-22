import os
from dotenv import load_dotenv

load_dotenv('.env')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')
DATABASEURL = os.getenv('DATABASEURL')

