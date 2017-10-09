from os import environ
from os.path import dirname, abspath, join

from dotenv import load_dotenv


BASE_DIR = dirname(dirname(abspath(__file__)))
load_dotenv(join(BASE_DIR, '.env'))

WATCHLIST_MAP = environ.get("WATCHLIST_MAP").replace(" ", "").split("|")
PERIOD = int(environ.get("PERIOD"))
BROKER = environ.get("BROKER")
USERID = int(environ.get("XTB_USER"))
PASSWORD = environ.get("XTB_PASSWORD")
API = environ.get("API_URL")
USE_LOCAL = int(environ.get("USE_LOCAL"))
DATA_FOLDER = join(environ.get("USERPROFILE"), "AppData", "Roaming", 
    "MetaQuotes", "Terminal", environ.get("DATA_FOLDER"), "MQL4", "Files")
