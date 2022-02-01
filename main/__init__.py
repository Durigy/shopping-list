from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import timedelta
from main.config import secret_key, database_uri, debug_setting

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)
app.config['DEBUG'] = debug_setting

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# login_manager.init_app()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)

from main import routes