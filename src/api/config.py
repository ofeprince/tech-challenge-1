import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "db")

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    CACHE_TYPE = 'simple'
    SWAGGER = {
        'title': os.getenv('SWAGGER_TITLE'),
        'uiversion': 3
    }
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DATA_DIR, "booksraping.db")}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')
    ADMIN_USER = os.getenv('USER_ADMIN')
    PASS_ADMIN = os.getenv('PASS_ADMIN')