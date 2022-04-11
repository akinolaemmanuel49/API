import os

from dotenv import load_dotenv

# BASE_DIR = os.path.join(os.path.dirname(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
# load_dotenv(BASE_DIR)


class Settings:
    """
    Base Settings for the project.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL').replace("postgres", "postgresql", 1)
    ENCRYPTION_SCHEMES = ['bcrypt']
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
    JWT_EXPIRATION_MINUTES = int(os.environ.get('JWT_EXPIRATION_MINUTES'))
    JWT_REFRESH_EXPIRE_HOURS = int(os.environ.get('JWT_REFRESH_EXPIRE_HOURS'))
