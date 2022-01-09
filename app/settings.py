import os

from dotenv import load_dotenv

BASE_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(BASE_DIR)


class Settings:
    """
    Base Settings for the project.
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    ENCRYPTION_SCHEMES = ['bcrypt']
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_EXPIRATION_MINUTES = os.getenv('JWT_EXPIRATION_MINUTES')
    JWT_REFRESH_EXPIRE_HOURS = os.getenv('JWT_REFRESH_EXPIRE_HOURS')
