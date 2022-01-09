import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = os.environ.get('DEBUG', False)
    LOG_DIR = os.path.join(basedir, 'logs')
    LOG_TO_STDOUT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
