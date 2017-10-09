from os import environ
from os.path import dirname, abspath, join

from dotenv import load_dotenv


BASE_DIR = dirname(dirname(abspath(__file__)))
load_dotenv(join(BASE_DIR, '.env'))

WATCHLIST = environ.get("WATCHLIST").replace(" ", "").split("|")
PERIOD = int(environ.get("PERIOD"))
USERID = environ.get("XTB_USER")
PASSWORD = environ.get("XTB_PASSWORD")
API = environ.get("API_URL")
DATA_FOLDER = environ.get("DATA_FOLDER")