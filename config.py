import os
with open('project/credentials/postgres_info.json') as db_file:
    data_base = json.load(db_file)

class config(object):

    SQLALCHEMY_DATABASE_URI = data_base['db_url']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = os.urandom(24)