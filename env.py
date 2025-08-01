import os
from dotenv import load_dotenv

load_dotenv()

class Env:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('DEBUG', 'True').lower() in ['true', '1', 'yes']
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    API_VERSION = os.getenv('API_VERSION', 'v1')
    ROOT_URLCONF = os.getenv('ROOT_URLCONF', 'metaafzar.urls')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'db.sqlite3')
    DATABASE_ENGINE = os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3')
    DATABASE_USER = os.getenv('DATABASE_USER', '')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '')


my_env = Env("development")  # Change to "production" or "staging" as needed

