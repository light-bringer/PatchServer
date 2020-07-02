import os

SECRET_KEY = os.urandom(32)

APP_DIR = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
SQL_LOGGING = False

DATABASE_PATH = os.path.join(
    os.environ.get('DATABASE_DIR', APP_DIR), 'patch_server.db')

if os.name == 'nt':
    SQLALCHEMY_DATABASE_URI = r'sqlite:///{}' .format(DATABASE_PATH)
    APP_DIR = APP_DIR.replace("\\", "\\\\")
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("\\", "\\\\")
else:
    SQLALCHEMY_DATABASE_URI = r'sqlite:////{}' .format(DATABASE_PATH)


SQLALCHEMY_TRACK_MODIFICATIONS = False
print("here is : ", APP_DIR, DATABASE_PATH, SQLALCHEMY_DATABASE_URI)
RESET_API_TOKEN = os.path.exists(os.path.join(APP_DIR, 'reset_api_token'))
