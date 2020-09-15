from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__ = "app_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80),nullable = False)
    user_id = db.Column(db.String())
    access_token = db.Column(db.String())
    refresh_token  = db.Column(db.String())
    token_type = db.Column(db.String())
    expires_in = db.Column(db.String())