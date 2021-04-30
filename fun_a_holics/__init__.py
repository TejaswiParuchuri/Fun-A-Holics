from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'd79cddc52783fe71bcbee0deb14061d0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@hostname:3306/databasename'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from fun_a_holics import routes