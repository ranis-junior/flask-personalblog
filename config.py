import os
from distutils.util import strtobool
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'key'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default='sqlite:///' + os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = strtobool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False'))
    SQLALCHEMY_ECHO = strtobool(os.getenv('SQLALCHEMY_ECHO', 'False'))

    # configurações de email
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 25)
    MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS', False))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    ADMINS = os.getenv('ADMINS', '').split(',')

    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT')

    # configurações de usabilidade
    POSTS_PER_PAGE = 10

    # configurações de traduções
    LANGUAGES = ['pt', 'en']

    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://')
