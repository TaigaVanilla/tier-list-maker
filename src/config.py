import os


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.urandom(24)


class ProductionConfig(Config):
    if os.getenv('DATABASE_URL') is not None:
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')

    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}


class DevelopmentConfig(Config):
    DEBUG = True

    SECRET_KEY = 'secret key'

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@db:5432/{db_name}'.format(
        **{
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'db_name': os.getenv('POSTGRES_DB'),
        }
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
