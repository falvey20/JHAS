import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '##########'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:########@localhost/JHASdb'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('JHAS_MAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('JHAS_MAIL_PASSWORD')
mail = Mail(app)


from blog import routes
