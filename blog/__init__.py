
from email.policy import default
from enum import unique
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import Config


app = Flask(__name__) 
app.config.from_object(Config)

db= SQLAlchemy(app) 
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = "users.login"             #login route accesses via the users Blueprints
loginManager.login_message_category ="info"     #to give it the bootstrap appearance(blue box)

mail = Mail(app)

from blog.users.routes import users                 #users, the name of blueprint instance with which all the routes are established
from blog.events.routes import events                  #posts, the name of blueprint instance with which all the routes are established
from blog.main.routes import main

#register the blueprint with the app
app.register_blueprint(users)
app.register_blueprint(events)
app.register_blueprint(main)


