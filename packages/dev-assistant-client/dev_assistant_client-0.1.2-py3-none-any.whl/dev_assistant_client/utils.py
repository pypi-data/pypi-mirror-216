import os
from dotenv import load_dotenv
load_dotenv()

APP_URL = os.getenv('APP_URL').replace('https://', '').replace('/', '')
API_PATH = '/api'
TOKEN_FILE = os.path.expanduser("~/.dev_assistant_token")
USER_DATA = os.path.expanduser("~/.dev_assistant_user")
PUSHER_APP_ID = os.getenv('PUSHER_APP_ID')
PUSHER_APP_KEY = os.getenv('PUSHER_APP_KEY')
PUSHER_APP_SECRET = os.getenv('PUSHER_APP_SECRET')
PUSHER_HOST = os.getenv('PUSHER_HOST')
PUSHER_PORT = os.getenv('PUSHER_PORT') or 443
PUSHER_SCHEME = os.getenv('PUSHER_SCHEME') or 'https'
PUSHER_APP_CLUSTER = os.getenv('PUSHER_APP_CLUSTER') or 'sa1'