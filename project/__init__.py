from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
login = LoginManager()
def init_app():
    """建構core flask app."""
    app = Flask(__name__,instance_relative_config=False, template_folder='templates')
    app.config.from_object(config)
    bootstrap = Bootstrap(app)
    db.init_app(app)
    login.init_app(app)
    with app.app_context():
        """ Import part of our core Flask app. """
        from . import routes
        from .dash.dashboard import init_dashboard
        app = init_dashboard(app)
        return app