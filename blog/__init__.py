from email.policy import default
from enum import unique
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = "17b65ec1ce5b91a8c73e39e04e56f80ba2cda099"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
 
db= SQLAlchemy(app) 
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = "login"
loginManager.login_message_category ="info"     #to give it the bootstrap appearance(blue box)


#routes file uses the app so importing the routes into this file at the top will give a circular import issue,
#hence import the routes after app has been made!
from blog import routes
