import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '3er5tte4b55q23c2y4afvfw41wrnp2zr84yys9ca92wam20js6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager()
login_manager.login_message = "Por favor, inicie sesión para ver este contenido"
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flask_mail import Mail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_MALIGNO')
app.config['MAIL_PASSWORD'] = os.environ.get('CLAVE_MALIGNA')
mail = Mail(app)

from blog import routes
