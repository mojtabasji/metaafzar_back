import os
from dotenv import load_dotenv

load_dotenv()


class Env:
    def __init__(self, environment="development"):
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', environment)

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('DEBUG', 'True').lower() in ['true', '1', 'yes']
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
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

if __name__ == "__main__":
    print("Environment Configuration:")
    print(f"ENVIRONMENT: {my_env.ENVIRONMENT}")
    print(f"SECRET_KEY: {my_env.SECRET_KEY}")
    print(f"DEBUG: {my_env.DEBUG}")
    print(f"ALLOWED_HOSTS: {my_env.ALLOWED_HOSTS}")
    print(f"DATABASE_URL: {my_env.DATABASE_URL}")
    print(f"API_VERSION: {my_env.API_VERSION}")
    print(f"ROOT_URLCONF: {my_env.ROOT_URLCONF}")
    print(f"DATABASE_NAME: {my_env.DATABASE_NAME}")
    print(f"DATABASE_ENGINE: {my_env.DATABASE_ENGINE}")
    print(f"DATABASE_USER: {my_env.DATABASE_USER}")
    print(f"DATABASE_PASSWORD: {my_env.DATABASE_PASSWORD}")
    print(f"DATABASE_HOST: {my_env.DATABASE_HOST}")
    print(f"DATABASE_PORT: {my_env.DATABASE_PORT}")