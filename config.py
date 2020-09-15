import os

class config(object):

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:20130203peien@localhost:5432/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = os.urandom(24)