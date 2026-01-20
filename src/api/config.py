import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get('VERCEL'):
    DB_PATH = '/tmp'
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DATA_DIR, exist_ok=True)

    DATA_DIR = os.path.join(DATA_DIR, "db")
    os.makedirs(DATA_DIR, exist_ok=True)
    DB_PATH = DATA_DIR

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    CACHE_TYPE = 'simple'
    SWAGGER = {
        'title': os.getenv('SWAGGER_TITLE'),
        'uiversion': 3
    }
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DB_PATH, 'booksraping.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')
    ADMIN_USER = os.getenv('USER_ADMIN')
    PASS_ADMIN = os.getenv('PASS_ADMIN')