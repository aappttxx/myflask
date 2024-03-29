import os

from app import app

dev_db = 'sqlite:///' + \
    os.path.join(os.path.dirname(app.root_path), 'data.sqlite')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
