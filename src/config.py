import os


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')


class ProductionConfig(Config):
    pass


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
