from project.model import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
db = SQLAlchemy()


def token_saver(token):
    user = db.session.query(User).filter_by(username=current_user.username).first()
    user.access_token = token['access_token']
    user.token_type = token['token_type']
    user.refresh_token = token['refresh_token']
    user.expires_in = token['expires_in']
    db.session.commit()